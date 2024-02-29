package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"syscall"

	"backend/configs"
	"backend/internal/restapi"
	"backend/internal/httpserver"
	"backend/internal/rabbitmq/publisher"
)

func main() {
	cfg, err := configs.NewConfig()
	if err != nil {
		log.Fatalf("error while setting config: %v\n", err)
	}

	p, err := publisher.NewRabbitmqPublisher(cfg.RabbitParams.RabbitUrl)
	if err != nil {
		log.Fatalf("error while creating publisher: %v\n", err)
	}
	defer p.Close()

	s := restapi.NewRestapiService(
		cfg.EstimationParams.Host, 
		cfg.EstimationParams.Port,
	)

	server := httpserver.NewServer(p, s)

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	go func() {
		if err := server.Listen(ctx); err != nil {
			log.Fatalf("server error: %v\n", err)
		}
	}()

	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)

	sig := <-c
	log.Printf("received %v signal\n", sig)
	cancel()
	
	<-ctx.Done()
}
