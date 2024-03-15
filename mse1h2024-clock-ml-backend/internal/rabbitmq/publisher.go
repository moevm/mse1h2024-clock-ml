package rabbitmq

import (
	"backend/internal/logger"
	"context"
	"log/slog"

	amqp "github.com/rabbitmq/amqp091-go"
)

// Publisher instance of rabbitmq.
type Publisher struct {
	connection *amqp.Connection
	channel    *amqp.Channel
}

// PublishMessage publishes a message to the specified rabbitmq queue.
func (p *Publisher) PublishMessage(ctx context.Context, queueName string, messageBody []byte) error {
	_, err := p.channel.QueueDeclare(
		queueName,
		false,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		return err
	}

	err = p.channel.PublishWithContext(
		ctx,
		"",
		queueName,
		false,
		false,
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        messageBody,
		},
	)

	if err != nil {
		logger.Log(ctx, slog.LevelInfo, "failed to publish message to rabbitmq", slog.Any("error", err))
		return ErrInvalidPublishing
	}

	return nil
}

// Close closes the rabbitmq connection and channel.
func (p *Publisher) Close() {
	p.connection.Close()
	p.channel.Close()
}

// New creates a new Publisher instance.
func New(addr string) (Publisher, error) {
	conn, err := amqp.Dial(addr)
	if err != nil {
		return Publisher{}, err
	}

	ch, err := conn.Channel()
	if err != nil {
		return Publisher{}, err
	}

	return Publisher{
		connection: conn,
		channel:    ch,
	}, nil
}
