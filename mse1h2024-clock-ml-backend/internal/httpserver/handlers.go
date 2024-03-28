package httpserver

import (
	"encoding/json"
	"log/slog"
	"net/http"
	"strconv"
	"io"
	
	"backend/internal/logger"
	"backend/internal/rabbitmq"
	"backend/internal/restapi"
)

const (
	queueName   = "estimation"
	brokerParam = "broker"
	fileParam   = "file"
)

// SendPicture processes requests for sending pictures using AMQP or REST, based on 'broker' queryParam.
func SendPicture(rabbit rabbitmq.Publisher, rest restapi.Service) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		err := r.ParseMultipartForm(10 << 20) // 10 MB max
		if err != nil {
			logger.Log(r.Context(), slog.LevelInfo, "failed to read request body", slog.Any("error", err))
			httpError(w, "invalid body of request", http.StatusBadRequest)
			return
		}

		file, handler, err := r.FormFile(fileParam)

		if err != nil {
			logger.Log(r.Context(), slog.LevelInfo, "failed to get file from request", slog.Any("error", err))
			httpError(w, "invalid file", http.StatusBadRequest)
			return
		}
		defer file.Close()

		if handler.Size == 0 {
			httpError(w, "file should not be empty", http.StatusBadRequest)
			return
		}

		var request ImageRequest

		request.IsBroker, err = strconv.ParseBool(r.FormValue(brokerParam))
		if err != nil {
			logger.Log(r.Context(), slog.LevelInfo, "failed to get broker param", slog.Any("error", err))
			httpError(w, "invalid broker param", http.StatusBadRequest)
			return
		}

		request.Image, err = io.ReadAll(file)
		if err != nil {
			logger.Log(r.Context(), slog.LevelInfo, "failed to read file", slog.Any("error", err))
			httpError(w, "internal server error", http.StatusInternalServerError)
			return
		}

		var result int
		if request.IsBroker {
			logger.Log(r.Context(), slog.LevelInfo, "sending image using rabbitmq")
			err := rabbit.PublishMessage(r.Context(), queueName, request.Image)
			if err != nil {
				httpError(w, err.Error(), http.StatusInternalServerError)
				return
			}
		} else {
			logger.Log(r.Context(), slog.LevelInfo, "sending image using restapi")
			result, err = rest.SendPictureRequest(r.Context(), request.Image)
			if err != nil {
				httpError(w, err.Error(), http.StatusInternalServerError)
				return
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
