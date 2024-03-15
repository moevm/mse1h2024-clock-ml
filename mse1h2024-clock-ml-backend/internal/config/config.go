package config

import (
	"io"
	"log"
	"os"

	"gopkg.in/yaml.v3"
)

const configEnv = "CFG_PATH"

type Config struct {
	App    App      `yaml:"app"`
	HTTP   HTTP     `yaml:"http"`
	Rabbit RabbitMQ `yaml:"rabbitmq"`
	REST   REST     `yaml:"estimation"`
}

type App struct {
	Name    string `yaml:"name" default:"mse1h2024-clock-ml-backend"`
	Version string `yaml:"version" default:"1.0.0"`
}

type HTTP struct {
	Port int `yaml:"port"`
}

type RabbitMQ struct {
	URL string `yaml:"url"`
}

type REST struct {
	Port int    `yaml:"port"`
	Host string `yaml:"host"`
}

// New returns parsed yaml-file from path in env CFG_PATH.
func New() (*Config, error) {
	file, err := os.Open(os.Getenv(configEnv))
	if err != nil {
		log.Fatalf("Error opening YAML file: %v", err)
		return nil, err
	}
	defer file.Close()

	data, err := io.ReadAll(file)
	if err != nil {
		log.Fatalf("Error reading YAML file: %v", err)
		return nil, err
	}

	var cfg Config
	err = yaml.Unmarshal(data, &cfg)
	if err != nil {
		log.Fatalf("Error unmarshalling YAML: %v", err)
		return nil, err
	}

	return &cfg, nil
}
