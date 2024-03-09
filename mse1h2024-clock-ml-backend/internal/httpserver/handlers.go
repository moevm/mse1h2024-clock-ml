package httpserver

import (
	"encoding/json"
	"net/http"
	"strconv"

	"backend/internal/logger"
	"backend/internal/rabbitmq/publisher"
	"backend/internal/restapi"
)
//todo test all
//todo add all doc
const (
	brokerQueryParam = "broker"
	queueName        = "estimation"
)

type Handlers struct {
	publisher publisher.RabbitmqPublisher
	service   restapi.Service
	log       *logger.Logger
}

func NewHandlers(
	rabbirPublisher publisher.RabbitmqPublisher,
	apiService restapi.Service,
	logger *logger.Logger,
) Handlers {
	return Handlers{
		publisher: rabbirPublisher,
		service:   apiService,
		log:       logger,
	}
}

// SendPicture processes requests for sending pictures using AMQP or REST, based on 'broker' queryParam.
func (handlers *Handlers) SendPicture() func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		isBroker, err := strconv.ParseBool(r.URL.Query().Get(brokerQueryParam))
		if err != nil {
			handleError(handlers.log, w, "Failed to parse 'broker' query parameter", http.StatusInternalServerError)
			return
		}

		var imageRequest ImageRequest
		if err := handlers.decodeJSON(r, &imageRequest); err != nil {
			handleError(handlers.log, w, "Failed to decode JSON", http.StatusInternalServerError)
			return
		}

		messageBody, err := json.Marshal(imageRequest)
		if err != nil {
			handleError(handlers.log, w, "Failed to marshal JSON", http.StatusInternalServerError)
			return
		}

		var sendFunc func() error
		if isBroker {
			sendFunc = func() error {
				return handlers.publisher.PublishMessage(queueName, messageBody)
			}
		} else {
			sendFunc = func() error {
				return handlers.service.SendPictureRequest(messageBody)
			}
		}

		if err := sendFunc(); err != nil {
			handleError(
				handlers.log,
				w,
				"Failed to send picture request",
				http.StatusInternalServerError,
			)
			return
		}

		w.WriteHeader(http.StatusOK)
	}
}

func (handlers *Handlers) decodeJSON(r *http.Request, v interface{}) error {
	return json.NewDecoder(r.Body).Decode(v)
}

func handleError(log *logger.Logger, w http.ResponseWriter, errorMessage string, statusCode int) {
	log.Error(errorMessage)
	http.Error(w, "internal server error", statusCode)
}
