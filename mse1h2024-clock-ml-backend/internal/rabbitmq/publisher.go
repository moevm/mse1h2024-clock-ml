package rabbitmq

import (
	"backend/internal/logger"
	"bytes"
	"context"
	"github.com/google/uuid"
	"log/slog"
	"strconv"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)

const queueName = "estimation"

// Publisher instance of rabbitmq.
type Publisher struct {
	connection *amqp.Connection
	channel    *amqp.Channel
}

// PublishMessage publishes a message to the specified rabbitmq queue.
func (p *Publisher) PublishMessage(ctx context.Context, body *bytes.Buffer, contentType string) (int, error) {
	q, err := p.channel.QueueDeclare(
		"",
		false,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		return 0, err
	}

	correlationID := uuid.New().String()

	msgs, err := p.channel.Consume(
		q.Name,
		"",
		true,  // autoAck
		true,  // exclusive
		false, // noLocal
		false, // noWait
		nil,   // args
	)
	if err != nil {
		logger.Log(ctx, slog.LevelInfo, "failed to consume rabbit mq", slog.Any("error", err))
		return 0, ErrInvalidPublishing
	}

	subCtx, cancel := context.WithTimeout(ctx, 60*time.Second)
	defer cancel()
	err = p.channel.PublishWithContext(
		subCtx,
		"",
		queueName,
		false,
		false,
		amqp.Publishing{
			ContentType:   contentType,
			CorrelationId: correlationID,
			ReplyTo:       q.Name,
			Body:          body.Bytes(),
		},
	)

	if err != nil {
		logger.Log(ctx, slog.LevelInfo, "failed to publish message to rabbitmq", slog.Any("error", err))
		return 0, ErrInvalidPublishing
	}

	var result int
	for msg := range msgs {
		if msg.CorrelationId != correlationID {
			continue
		}

		ans := string(msg.Body)
		result, err = strconv.Atoi(ans)
		if err != nil {
			logger.Log(ctx, slog.LevelInfo, "got error answer from ml service", slog.Any("answer", ans))
			return 0, ErrInvalidPublishing
		}

		return result, nil
	}

	logger.Log(ctx, slog.LevelWarn, "got no from ml service")
	return 0, ErrInvalidPublishing
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
