package restapi

import "errors"

var (
	ErrInvalidRequest  = errors.New("invalid estimation request")
	ErrInvalidResponce = errors.New("estimation service returned non-OK status")
)
