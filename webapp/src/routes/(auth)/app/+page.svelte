<script lang="ts">
	import { page } from '$app/stores';
	import type { Guild } from '$controllers/ipc';

	export let data: { guilds: Promise<Guild[]> };
</script>

{#await data.guilds}
	<div class="grid md:grid-cols-5 md:gap-5 mx-2">
		{#each Array(10) as _}
			<a href="." class="block">
				<div class="text-center border-white border-2 overflow-auto rounded-md">
					<div class="font-bold sticky top-0 w-full bg-black flex justify-center">
						<div class="animate-pulse rounded-md bg-gray-300 m-1 h-4 w-[100px]" />
					</div>
					<div class="h-48 w-full animate-pulse bg-gray-300"></div>
				</div>
			</a>
		{/each}
	</div>
{:then guilds}
	{#if guilds.length === 0}
		<div class="flex items-center justify-center h-screen">
			<div class="bg-black text-2xl font-bold py-40 px-48 rounded-lg">
				You are not in any of the configured server
			</div>
		</div>
	{:else}
		<div class="grid md:grid-cols-5 md:gap-5 mx-2">
			{#each guilds as guild}
				<a href="{$page.url.pathname}/{guild.id}">
					<div class="text-center border-white border-2 overflow-auto rounded-md">
						<div class="server-name font-bold sticky top-0 bg-black">{guild.name}</div>
						<img
							class="w-full object-cover"
							alt={guild.icon}
							src={guild.icon
								? `//cdn.discordapp.com/icons/${guild.id}/${guild.icon}.png`
								: '//global-img.gamergen.com/logo-gg-discord-1_0000932383.jpg'}
						/>
					</div>
				</a>
			{/each}
		</div>
	{/if}
{/await}
