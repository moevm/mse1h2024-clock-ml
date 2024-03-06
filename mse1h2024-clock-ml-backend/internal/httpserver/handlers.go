package httpserver

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"

	"backend/internal/rabbitmq"
	"backend/internal/rabbitmq/publisher"
	"backend/internal/restapi"
)

const (
	brokerQueryParam = "broker"
	queueName = "estimation"
)

// SendPicture processes requests for sending pictures using amqp or rest, based on 'broker' queryParam.
func SendPicture(
	publisher publisher.RabbitmqPublisher,
	service restapi.RestapiService,
) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		isBroker := r.URL.Query().Get(brokerQueryParam)

		isBrokerValue, err := strconv.ParseBool(isBroker)
		if err != nil {
			http.Error(
				w,
				"invalid broker boolean parameter",
				http.StatusBadRequest,
			)
			return
		}

		var imageRequest ImageRequest
		if err := decodeJSON(r, &imageRequest); err != nil {
			http.Error(w, "invalid JSON format", http.StatusBadRequest)
			return
		}

		messageBody, err := json.Marshal(imageRequest)
		if err != nil {
			http.Error(
				w,
				"failed to marshal JSON",
				http.StatusInternalServerError,
			)
			return
		}

		if isBrokerValue {
			err = publisher.PublishMessage(queueName, messageBody)
		} else {
			err = service.SendPictureRequest(messageBody)
		}

		handleError(w, err)
	}
}

func decodeJSON(r *http.Request, v interface{}) error {
	return json.NewDecoder(r.Body).Decode(v)
}

func handleError(w http.ResponseWriter, err error) {
	switch err {
	case restapi.ErrInvalidRequest:
		http.Error(
			w,
			"invalid estimation request",
			http.StatusBadRequest,
		)
		return
	case restapi.ErrInvalidResponse:
		http.Error(
			w,
			"estimation service returned non-OK status",
			http.StatusBadGateway,
		)
	case rabbitmq.ErrInvalidPublishing:
		http.Error(
			w,
			fmt.Sprintf("invalid publishing in queue: %s", queueName),
			http.StatusBadGateway,
		)
	case rabbitmq.ErrInvalidQueueDeclare:
		http.Error(
			w,
			fmt.Sprintf("invalid declare queue: %s", queueName),
			http.StatusInternalServerError,
		)
	default:
		w.WriteHeader(http.StatusOK)
	}
}
