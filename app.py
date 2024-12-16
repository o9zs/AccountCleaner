import asyncio

from rich.console import Console

from telethon import TelegramClient

import config

client = TelegramClient("telethon", config.API_ID, config.API_HASH, system_version="5.9")

console = Console(highlight=False)

options = {
	1: "leave groups",	
	2: "leave channels",
	3: "delete conversations",
	4: "clear favorites"
}

console.log("\n".join([f"[bold]{number}[/bold] - {text}" for number, text in options.items()]))

selected_options = console.input("\nSelect all desired options: ")

async def main():
	if "1" in selected_options:
		console.log("\n[italic]Leaving groups...[/italic]")

		async for dialog in client.iter_dialogs():
			if dialog.is_group:
				await client.delete_dialog(dialog)

				console.log(f"Left [bold]{dialog.name}[/bold]")

				await asyncio.sleep(config.interval)

	if "2" in selected_options:
		console.log("\n[italic]Leaving channel...[/italic]")

		async for dialog in client.iter_dialogs():
			if dialog.is_channel:
				await client.delete_dialog(dialog)

				console.log(f"Left [bold]{dialog.name}[/bold]")

				await asyncio.sleep(config.interval)

	if "3" in selected_options:
		console.log("\n[italic]Deleting conversations...[/italic]")

		async for dialog in client.iter_dialogs():
			if dialog.is_private:
				await client.delete_dialog(dialog)

				console.log(f"Deleted conversation with [bold]{dialog.name}[/bold]")

				await asyncio.sleep(config.interval)

	if "4" in selected_options:
		console.log("\n[italic]Clearing favorites...[/italic]")

		async for message in client.iter_messages("@me"):
			message.delete()

			console.log(f"Delete message with ID [bold]{message.id}[/bold]")

			await asyncio.sleep(config.interval)

with client:
    client.loop.run_until_complete(main())