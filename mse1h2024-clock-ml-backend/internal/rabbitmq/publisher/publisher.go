package publisher

import (
	"context"

	amqp "github.com/rabbitmq/amqp091-go"
)

type RabbitmqPublisher struct {
	connection *amqp.Connection
	channel    *amqp.Channel
}


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
		return err
	}
	
	return nil
}

func (p *RabbitmqPublisher) Close() {
	p.connection.Close()
	p.channel.Close()
}

func NewRabbitmqPublisher(addr string) (RabbitmqPublisher, error) {
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