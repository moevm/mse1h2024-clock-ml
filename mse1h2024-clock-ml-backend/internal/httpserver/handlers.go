package httpserver

import (
	"backend/internal/logger"
	"backend/internal/rabbitmq"
	"backend/internal/restapi"
	"encoding/json"
	"log/slog"
	"net/http"
	"strconv"
)

const (
	brokerQueryParam = "broker"
	queueName        = "estimation"
)

// SendPicture processes requests for sending pictures using AMQP or REST, based on 'broker' queryParam.
func SendPicture(rabbit rabbitmq.Publisher, rest restapi.Service) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		isBroker, err := strconv.ParseBool(r.URL.Query().Get(brokerQueryParam))
		if err != nil {
			logger.Log(
				r.Context(), slog.LevelError,
				"failed to parse 'broker' query parameter",
				slog.Any("error", err),
			)
			httpError(w, "invalid broker argument", http.StatusBadRequest)
			return
		}

		var body []byte
		_, err = r.Body.Read(body)
		if err != nil {
			logger.Log(
				r.Context(),
				slog.LevelError,
				"failed to read request body",
				slog.Any("error", err),
			)
			httpError(w, "invalid body of request", http.StatusBadRequest)
			return
		}

		var imageRequest ImageRequest
		if err = json.NewDecoder(r.Body).Decode(&imageRequest); err != nil {
			logger.Log(
				r.Context(),
				slog.LevelError,
				"failed to parse JSON from body",
				slog.Any("error", err),
			)
			httpError(w, "invalid JSON body", http.StatusBadRequest)
			return
		}

		if imageRequest.Metadata.Width == 0 || imageRequest.Metadata.Height == 0 {
			logger.Log(r.Context(), slog.LevelInfo, "invalid image size")
			httpError(w, "invalid image size", http.StatusBadRequest)
			return
		}

		var result int
		if isBroker {
			logger.Log(r.Context(), slog.LevelInfo, "sending image using rabbitmq")
			err := rabbit.PublishMessage(r.Context(), queueName, body)
			if err != nil {
				httpError(w, err.Error(), http.StatusInternalServerError)
			}
		} else {
			logger.Log(r.Context(), slog.LevelInfo, "sending image using rest")
			result, err = rest.SendPictureRequest(r.Context(), body)
			if err != nil {
				httpError(w, err.Error(), http.StatusInternalServerError)
			}
		}

		w.WriteHeader(http.StatusOK)
		w.Header().Set("Content-Type", "application/json; charset=utf-8")
		err = json.NewEncoder(w).Encode(SuccessResponse{Result: result})
		if err != nil {
			logger.Log(r.Context(), slog.LevelError, "error during encoding response", slog.Any("error", err))
		}
	}
}

func httpError(w http.ResponseWriter, message string, code int) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(code)
	_ = json.NewEncoder(w).Encode(ErrorResponse{Message: message})
}
