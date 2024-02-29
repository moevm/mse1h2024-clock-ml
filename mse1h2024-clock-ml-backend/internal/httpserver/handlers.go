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
	paramName = "broker"
	queueName = "estimation"
)

// Processes requests for sending pictures using amqp or rest, based on 'broker' queryParam.
func SendPicture(
	p publisher.RabbitmqPublisher,
	s restapi.RestapiService,
) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		queryParams := r.URL.Query()
		isBroker := queryParams.Get(paramName)

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
				"Failed to marshal JSON",
				http.StatusInternalServerError,
			)
			return
		}

		if isBrokerValue {
			err = p.PublishMessage(queueName, messageBody)
		} else {
			err = s.SendPictureRequest(messageBody)
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
	case restapi.ErrInvalidResponce:
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
