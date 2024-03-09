package publisher

import (
	"context"

	"backend/internal/rabbitmq"

	amqp "github.com/rabbitmq/amqp091-go"
)

// RabbitmqPublisher instance of rabbitmq.
type RabbitmqPublisher struct {
	connection *amqp.Connection
	channel    *amqp.Channel
}

// PublishMessage publishes a message to the specified rabbitmq queue.
func (p *RabbitmqPublisher) PublishMessage(
	queueName string, messageBody []byte,
) error {
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
		context.Background(),
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
		return rabbitmq.ErrInvalidPublishing
	}

	return nil
}

// Close closes the rabbitmq connection and channel.
func (p *RabbitmqPublisher) Close() {
	p.connection.Close()
	p.channel.Close()
}

// New creates a new RabbitmqPublisher instance.
func New(addr string) (RabbitmqPublisher, error) {
	conn, err := amqp.Dial(addr)
	if err != nil {
		return RabbitmqPublisher{}, err
	}

	ch, err := conn.Channel()
	if err != nil {
		return RabbitmqPublisher{}, err
	}

	return RabbitmqPublisher{
		connection: conn,
		channel:    ch,
	}, nil
}
