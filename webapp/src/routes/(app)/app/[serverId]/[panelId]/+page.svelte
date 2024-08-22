<script lang="ts">
	import type { PageServerData } from './$types';

	export let data: PageServerData;
</script>

{#await data.messages}
	Loading messages
{:then messages}
	{#if messages.length === 0}
		<div class="flex items-center justify-center h-screen">
			<div class="bg-black text-2xl font-bold py-40 px-48 rounded-lg">
				No messages found in this panel
			</div>
		</div>
	{:else}
		<div class="grid grid-cols-5 gap-5 mx-2">
			{#each messages as message}
				<div class="text-center border-white border-2 overflow-auto rounded-md">
					<img
						class="rounded-full"
						alt={message.userName}
						src="//global-img.gamergen.com/logo-gg-discord-1_0000932383.jpg"
					/>
					<div class="server-name font-bold sticky top-0 bg-black">{message.userName}</div>
					<div class="server-name font-bold sticky top-0 bg-black">{message.message}</div>
				</div>
			{/each}
		</div>
	{/if}
{/await}
