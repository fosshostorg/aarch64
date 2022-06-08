/* SPDX-License-Identifier: BSD 2-Clause "Simplified" License
 *
 * Created by:	Aakash Sen Sharma, May 2022
 * Copyright:	(C) 2022, Aakash Sen Sharma & Contributors
 */
package main

import (
	"github.com/gofiber/fiber/v2"
)

func main() {
	app := fiber.New(fiber.Config{
		Prefork:       true,
		CaseSensitive: false,
		StrictRouting: false,
		ServerHeader:  "fosshost-aarch64",
		AppName:       "Aarch64 API",
	})

	app.Get("/", func(c *fiber.Ctx) error {
		return c.SendString("Hello, World 👋!")
	})

	app.Listen(":3000")
}
