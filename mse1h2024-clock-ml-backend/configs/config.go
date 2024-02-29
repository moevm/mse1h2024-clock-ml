package configs

import (
	"io"
	"log"
	"os"
	"sync"

	"gopkg.in/yaml.v3"
)

var (
	ConfigPath = os.Getenv("CFG_PATH")
	once       sync.Once
	instance   *Config
)

type Config struct {
	AppInfo          App        `yaml:"app"`
	HttpParams       HTTP       `yaml:"http"`
	RabbitParams     RabbitMQ   `yaml:"rabbitmq"`
	EstimationParams Estimation `yaml:"estimation"`
}

type App struct {
	Name    string `yaml:"name" default:"mse1h2024-clock-ml-backend"`
	Version string `yaml:"version" default:"1.0.0"`
}

type HTTP struct {
	Port int `yaml:"port"`
}

type RabbitMQ struct {
	RabbitUrl string `yaml:"url"`
}

type Estimation struct {
	Port int    `yaml:"port"`
	Host string `yaml:"host"`
}

// / NewConfig creates a singleton instance of the Config struct.
func NewConfig() (*Config, error) {
	once.Do(func() {
		file, err := os.Open(ConfigPath)
		if err != nil {
			log.Fatalf("Error opening YAML file: %v", err)
			instance = nil
			return
		}
		defer file.Close()

		data, err := io.ReadAll(file)
		if err != nil {
			log.Fatalf("Error reading YAML file: %v", err)
			instance = nil
			return
		}

		var cfg Config
		err = yaml.Unmarshal(data, &cfg)
		if err != nil {
			log.Fatalf("Error unmarshalling YAML: %v", err)
			instance = nil
			return
		}

		instance = &cfg
	})

	return instance, nil
}
