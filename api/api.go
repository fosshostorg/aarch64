/* SPDX-License-Identifier: BSD 2-Clause "Simplified" License
 *
 * Created by:	Aakash Sen Sharma, May 2022
 * Copyright:	(C) 2022, Aakash Sen Sharma & Contributors
 */
package main

import (
	"github.com/gofiber/fiber/v2"
	"github.com/joho/godotenv"
	"go.uber.org/zap"
)

func main() {
	// Setup zap logger.
	logger, _ := zap.NewDevelopment()
	defer logger.Sync()

	// Load .env configuration.
	if err := godotenv.Load(); err != nil {
		logger.Error("Error loading .env file", zap.String("Error", err.Error()))
	}

	// Creating the API instance.
	api := fiber.New(fiber.Config{
		Prefork:       false,
		CaseSensitive: false,
		StrictRouting: false,
		ServerHeader:  "fosshost-aarch64",
		AppName:       "Aarch64 API",
	})

	// Register routes.
	api.Get("/", func(c *fiber.Ctx) error {
		return c.SendString("Hello, World 👋!")
	})

	// Start the api.
	api.Listen(":3000")
}
