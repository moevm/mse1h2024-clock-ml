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
func (s *Service) SendPictureRequest(ctx context.Context, messageBody []byte) error {
	resp, err := http.Post(s.Url, "application/json", bytes.NewBuffer(messageBody))
	if err != nil {
		logger.Log(ctx, slog.LevelError, "failed to send picture request", slog.Any("error", err))
		return ErrInvalidRequest
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK || resp.StatusCode == http.StatusNoContent {
		return nil
	}

	return handleErrorResponse(ctx, resp.Body)
}

func handleErrorResponse(ctx context.Context, body io.ReadCloser) error {
	respData, err := io.ReadAll(body)
	if err != nil {
		logger.Log(ctx, slog.LevelError, "failed to read response body", slog.Any("error", err))
		return ErrInvalidResponse
	}

	var response Response
	err = json.Unmarshal(respData, &response)
	if err != nil {
		logger.Log(ctx, slog.LevelWarn, "failed to unmarshall response body", slog.Any("error", err))
		return ErrInvalidResponse
	}

	if response.Error != "" {
		return errors.New(response.Error)
	}

	return nil
}

// New creates a new Service instance.
func New(host string, port int) Service {
	url := fmt.Sprintf(estimationURLFmt, host, port)

	return Service{
		Url: url,
	}
}
