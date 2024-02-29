package rabbitmq

import "errors"

var (
	ErrInvalidPublishing   = errors.New("error while publishing message")
	ErrInvalidQueueDeclare = errors.New("error while declare queue")
)
