package restapi

import (
	"bytes"
	"fmt"
	"net/http"
)

type RestapiService struct {
	Url string
}

// Send request with encoded picture to estimation
func (s *RestapiService) SendPictureRequest(
	messageBody []byte,
) error {
	resp, err := http.Post(s.Url, "application/json", bytes.NewBuffer(messageBody))
	if err != nil {
		return ErrInvalidRequest
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return ErrInvalidResponce
	}

	return nil
}

// Creates a new RestapiService instance.
func NewRestapiService(host string, port int) RestapiService {
	url := fmt.Sprintf(
		"http://%s:%d/process/estimation",
		host,
		port,
	)

	return RestapiService{
		Url: url,
	}
}
