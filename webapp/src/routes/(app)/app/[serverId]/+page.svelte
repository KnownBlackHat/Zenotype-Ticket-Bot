<script lang="ts">
	import { goto } from '$app/navigation';
	import type { Panel } from '$controllers/ipc';
	import { page } from '$app/stores';

	export let data: { panels: Promise<Panel[]> };
</script>

<button
	class="bg-green-500 p-2 border-2 border-white rounded-md m-2"
	on:click={() => goto(`${$page.url.pathname}/create`)}
>
	Create Panel
</button>
<hr />
<h1 class="text-center underline text-4xl m-4">Panels</h1>
{#await data.panels}
	<div class="grid md:grid-cols-5 md:gap-5 mx-2">
		{#each Array(10) as _}
			<div
				class="bg-blue-600 flex flex-col justify-center items-center hover:bg-black cursor-grab rounded-md border-white border-2 p-2 w-[15rem] h-[5rem] animate-pulse"
			>
				<div class="flex flex-col">
					<div class="animate-pulse rounded-md bg-gray-300 m-1 h-4 w-[200px]" />
					<div class="animate-pulse rounded-md bg-gray-300 m-1 h-4 w-[200px]" />
				</div>
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
		<div class="grid md:grid-cols-5 md:gap-5 m-2 align-center text-center">
			{#each panels as panel}
				<div
					class="bg-blue-600 hover:bg-black cursor-grab rounded-md border-white border-2 p-2 w-[15rem] h-[5rem]"
				>
					<a
						tabindex={panel.id}
						role="button"
						class="flex flex-col"
						href="{$page.url.pathname}/{panel.id}"
					>
						<span>Id: {panel.id}</span>
						<span>
							Title: {panel.title}
						</span>
					</a>
				</div>
			{/each}
		</div>
	{/if}
{:catch e}
	{e}
{/await}
