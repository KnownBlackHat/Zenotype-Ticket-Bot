<script lang="ts">
	import { goto } from '$app/navigation';
	import type { UserInfo } from '$controllers/user';
	export let data: UserInfo;
</script>

<div
	class="flex justify-between items-center mb-2 opacity-80"
	style="background-color: #{data.accent_color ?? '000000'}"
>
	<a on:click={() => history.back()} href=".">
		{#if data.avatar}
			<img
				title="Go back"
				src={`//cdn.discordapp.com/avatars/${data.id}/${data.avatar}.jpg`}
				alt={data.avatar}
				class="rounded-full w-[4rem] h-[4rem] ml-5 border-white border-2"
			/>
		{:else}
			<img
				src={'//cdn.discordapp.com/embed/avatars/0.png'}
				alt="0"
				class="rounded-full w-[4rem] h-[4rem] ml-5 border-white border-2"
			/>
		{/if}
	</a>
	<div class="text-xl font-bold md:text-3xl">{data.global_name ?? ''}</div>
	<button
		class="bg-black text-white m-4 rounded-md border-white border-2 text-center p-2"
		title="logout"
		on:click={() => {
			goto('/logout', { invalidateAll: true });
		}}>Logout</button
	>
</div>

<slot />
