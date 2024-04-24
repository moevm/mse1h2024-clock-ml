package httpserver

import (
	"backend/internal/logger"
	"backend/internal/rabbitmq"
	"backend/internal/restapi"
	"bytes"
	"encoding/json"
	"io"
	"log/slog"
	"mime/multipart"
	"net/http"
	"strconv"
)

const (
	brokerParam  = "broker"
	hoursParam   = "hours"
	minutesParam = "minutes"
	fileParam    = "file"
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

		request.Hours, err = strconv.Atoi(r.FormValue(hoursParam))
		if err != nil {
			logger.Log(r.Context(), slog.LevelInfo, "failed to get hours param", slog.Any("error", err))
			httpError(w, "invalid hours param", http.StatusBadRequest)
			return
		}

		request.Minutes, err = strconv.Atoi(r.FormValue(minutesParam))
		if err != nil {
			logger.Log(r.Context(), slog.LevelInfo, "failed to get minutes param", slog.Any("error", err))
			httpError(w, "invalid minutes param", http.StatusBadRequest)
			return
		}

		request.Image, err = io.ReadAll(file)
		if err != nil {
			logger.Log(r.Context(), slog.LevelInfo, "failed to read file", slog.Any("error", err))
			httpError(w, "internal server error", http.StatusInternalServerError)
			return
		}

		message, contentType, err := generateMessage(request)
		if err != nil {
			logger.Log(r.Context(), slog.LevelInfo, "failed to generate message for ml service", slog.Any("error", err))
			httpError(w, "internal server error", http.StatusInternalServerError)
			return
		}

		var result int
		if request.IsBroker {
			logger.Log(r.Context(), slog.LevelInfo, "sending image using rabbitmq")
			result, err = rabbit.PublishMessage(r.Context(), message, contentType)
		} else {
			logger.Log(r.Context(), slog.LevelInfo, "sending image using restapi")
			result, err = rest.SendPictureRequest(r.Context(), message, contentType)
		}

		if err != nil {
			httpError(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		w.Header().Set("Content-Type", "application/json; charset=utf-8")
		err = json.NewEncoder(w).Encode(SuccessResponse{Result: result})
		if err != nil {
			logger.Log(r.Context(), slog.LevelError, "error during encoding response", slog.Any("error", err))
		}
	}
}

func generateMessage(request ImageRequest) (*bytes.Buffer, string, error) {
	body := &bytes.Buffer{}

	writer := multipart.NewWriter(body)
	defer writer.Close()

	image, err := writer.CreateFormFile(fileParam, "image.png")
	if err != nil {
		return nil, "", err
	}

	_, err = image.Write(request.Image)
	if err != nil {
		return nil, "", err
	}

	err = writer.WriteField(hoursParam, strconv.Itoa(request.Hours))
	if err != nil {
		return nil, "", err
	}
	err = writer.WriteField(minutesParam, strconv.Itoa(request.Minutes))
	if err != nil {
		return nil, "", err
	}

	return body, writer.FormDataContentType(), nil
}

func httpError(w http.ResponseWriter, message string, code int) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(code)
	_ = json.NewEncoder(w).Encode(ErrorResponse{Message: message})
}
