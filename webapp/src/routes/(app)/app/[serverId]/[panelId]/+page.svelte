<script lang="ts">
	import type { PageServerData } from './$types';
	import { page } from '$app/stores';

	export let data: PageServerData;
</script>

{#await data.tickets}
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
{:then tickets}
	{#if tickets.length === 0}
		<div class="flex items-center justify-center h-screen">
			<div class="bg-black text-2xl font-bold py-40 px-48 rounded-lg">No tickets found</div>
		</div>
	{:else}
		<div class="grid md:grid-cols-5 md:gap-5 m-2 align-center text-center">
			{#each tickets as ticket}
				<div
					class="bg-blue-600 hover:bg-black cursor-grab rounded-md border-white border-2 p-2 w-[15rem] h-[5rem]"
				>
					<a
						tabindex={ticket.id}
						role="button"
						class="flex flex-col"
						href="{$page.url.pathname}/{ticket.id}"
					>
						<span>Id: {ticket.id}</span>
						<span>
							User Id: {ticket.userId}
						</span>
					</a>
				</div>
			{/each}
		</div>
	{/if}
{:catch e}
	{e}
{/await}
