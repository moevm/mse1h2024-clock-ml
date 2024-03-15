package restapi

import (
	"backend/internal/logger"
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log/slog"
	"net/http"
)

const estimationURLFmt = "http://%s:%d/process/estimation"

type Service struct {
	Url string
}

// SendPictureRequest sends request with encoded picture to estimation
func (s *Service) SendPictureRequest(ctx context.Context, messageBody []byte) (int, error) {
	resp, err := http.Post(s.Url, "application/json", bytes.NewBuffer(messageBody))
	if err != nil {
		logger.Log(ctx, slog.LevelError, "failed to send picture request", slog.Any("error", err))
		return 0, ErrInvalidRequest
	}
	defer resp.Body.Close()

	respData, err := io.ReadAll(resp.Body)
	if err != nil {
		logger.Log(ctx, slog.LevelError, "failed to read response body", slog.Any("error", err))
		return 0, ErrInvalidResponse
	}

	if resp.StatusCode != http.StatusOK {
		return 0, handleErrorResponse(ctx, respData)
	}

	var response SuccessResponse
	err = json.Unmarshal(respData, &response)
	if err != nil {
		logger.Log(ctx, slog.LevelWarn, "failed to unmarshall response body", slog.Any("error", err))
		return 0, ErrInvalidResponse
	}

	return response.Result, nil
}

func handleErrorResponse(ctx context.Context, body []byte) error {
	var response ErrorResponse
	err := json.Unmarshal(body, &response)
	if err != nil {
		logger.Log(ctx, slog.LevelWarn, "failed to unmarshall response body", slog.Any("error", err))
		return ErrInvalidResponse
	}

	return errors.New(response.Error)
}

// New creates a new Service instance.
func New(host string, port int) Service {
	url := fmt.Sprintf(estimationURLFmt, host, port)

	return Service{
		Url: url,
	}
}
