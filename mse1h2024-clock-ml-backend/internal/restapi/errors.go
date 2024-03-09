package restapi

import "errors"

var (
	ErrInvalidRequest  = errors.New("invalid estimation request")
	ErrInvalidResponse = errors.New("estimation service returned invalid response")
)

type Response struct {
	Message string `json:"result"`
	Error   string `json:"error,omitempty"`
}
