import asyncio

from rich.console import Console

from telethon import functions, TelegramClient

import config

client = TelegramClient("telethon", config.API_ID, config.API_HASH, system_version="5.9")

console = Console(highlight=False)

options = {
	1: "leave groups",	
	2: "leave channels",
	3: "delete bots",
	4: "block private chats",
	5: "delete private chats",
	6: "clear favorites",
	7: "don't logout"
}

async def main():
	if "1" in selected_options:
		console.log("\n[italic]Leaving groups...[/italic]")

		async for dialog in client.iter_dialogs():
			if dialog.is_group:
				await client.delete_dialog(dialog)

				console.log(f"Left [bold]{dialog.name}[/bold]")

				await asyncio.sleep(config.interval)

		console.log("\n")

	if "2" in selected_options:
		console.log("\n[italic]Leaving channels...[/italic]")

		async for dialog in client.iter_dialogs():
			if dialog.is_channel:
				await client.delete_dialog(dialog)

				console.log(f"Left [bold]{dialog.name}[/bold]")

				await asyncio.sleep(config.interval)

		console.log("\n")

	if "3" in selected_options:
		console.log("\n[italic]Deleting bots...[/italic]")

		async for dialog in client.iter_dialogs():
			if dialog.is_user and dialog.entity.bot:
				await client(functions.contacts.BlockRequest(
					id=dialog.id
				))

				await client.delete_dialog(dialog)

				console.log(f"Deleted bot [bold]{dialog.name}[/bold]")

				await asyncio.sleep(config.interval)

		console.log("\n")

	if "4" in selected_options:
		console.log("\n[italic]Blocking private chats...[/italic]")

		async for dialog in client.iter_dialogs():
			if dialog.is_user and not dialog.entity.bot:
				await client(functions.contacts.BlockRequest(
					id=dialog.id
				))

				console.log(f"Blocked [bold]{dialog.name}[/bold]")

				await asyncio.sleep(config.interval)

		console.log("\n")

	if "5" in selected_options:
		console.log("\n[italic]Deleting private chats...[/italic]")

		async for dialog in client.iter_dialogs():
			if dialog.is_user and not dialog.entity.bot:
				await client.delete_dialog(dialog)

				console.log(f"Deleted private chat with [bold]{dialog.name}[/bold]")

				await asyncio.sleep(config.interval)

		console.log("\n")

	if "6" in selected_options:
		console.log("\n[italic]Clearing favorites...[/italic]")

		async for message in client.iter_messages("me"):
			await message.delete()

			console.log(f"Delete message with ID [bold]{message.id}[/bold]")

			await asyncio.sleep(config.interval)

		console.log("\n")

	if "7" not in selected_options:
		await client.log_out()

with client:
	console.log("\n".join([f"[bold]{number}[/bold] - {text}" for number, text in options.items()]))

	selected_options = console.input("\nSelect all desired options: ")
	
	client.loop.run_until_complete(main())