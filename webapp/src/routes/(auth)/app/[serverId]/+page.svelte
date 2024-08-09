<script lang="ts">
	import { goto } from '$app/navigation';
	import type { Panel } from '$controllers/ipc';
	import { page } from '$app/stores';

	export let data: { panels: Promise<Panel[]> };
</script>

<button
	class="bg-green-500 p-2 border-2 border-white rounded-md mx-2"
	on:click={() => goto(`${$page.url.pathname}/create`)}
>
	Create Panel
</button>
{#await data.panels}
	<div class="grid md:grid-cols-5 md:gap-5 mx-2">
		{#each Array(10) as _}
			<div class="bg-black animate-pulse">
				<div />
				<div />
			</div>
		{/each}
	</div>
{:then panels}
	{#if panels.length === 0}
		<div class="flex items-center justify-center h-screen">
			<div class="bg-black text-2xl font-bold py-40 px-48 rounded-lg">
				No panels configured for this server
			</div>
		</div>
	{:else}
		<div class="grid md:grid-cols-5 md:gap-5 mx-2">
			{#each panels as panel}
				{panel.title}
				{panel.description}
			{/each}
		</div>
	{/if}
{/await}
