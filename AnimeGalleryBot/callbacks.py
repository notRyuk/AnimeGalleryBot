from AnimeGalleryBot import tg_client as bot
from telethon import events, Button
from AnimeGalleryBot.gogoanime import gogoanime as gogo

try:
    @bot.on(events.CallbackQuery)
    async def callback_for_anime(event):
        data = event.data.decode('utf-8')
        if 'lt:' in data:
            split_data = data.split(":")
            animeid = split_data[-1]
            await send_details(event, animeid)

        elif 'Download' in data:
            x = data.split(":")
            button2 = [[]]
            current_row = 0
            if int(x[2]) < 101:
                for i in range(int(x[2])):
                    button2[current_row].append(Button.inline(
                        str(i+1), data=f'ep:{i+1}:{x[1]}'))
                    if (i+1) % 5 == 0:
                        button2.append([])
                        current_row = current_row + 1
                await event.edit(
                    f'Choose Episode:',
                    buttons=button2
                )
            else:
                num_of_buttons = (int(x[2]) // 100)
                for i in range(num_of_buttons):
                    button2[current_row].append(Button.inline(
                        f'{i}01 - {i+1}00', data=f'btz:{i+1}00:{x[1]}'))
                    if (i+1) % 3 == 0:
                        button2.append([])
                        current_row = current_row + 1
                if int(x[2]) % 100 == 0:
                    pass
                else:
                    button2[current_row].append(Button.inline(
                        f'{num_of_buttons}01 - {x[2]}', data=f'etz:{x[2]}:{x[1]}'))
                await event.edit(
                    f'Choose Episode:',
                    buttons=button2
                )

        elif 'longdl:' in data:
            x = data.split(":")
            button2 = [[]]
            current_row = 0
            search_results = gogo.get_search_results(x[1])
            (names, ids) = format.format_search_results(search_results)
            for i in ids:
                if i[-25:] == x[2]:
                    id = i
                    break
            for i in range(int(x[3])):
                button2[current_row].append(Button.inline(
                    str(i+1), data=f'spp:{i+1}:{x[2]}:{x[1]}'))
                if (i+1) % 5 == 0:
                    button2.append([])
                    current_row = current_row + 1
            try:
                await event.edit(
                    f'Choose Episode:',
                    buttons=button2
                )
            except:
                pass
    
        elif 'btz:' in data:
            data_split = data.split(':')
            button3 = [[]]
            current_row = 0
            endnum = data_split[1]
            startnum = int(f'{int(endnum[0])-1}01')
            for i in range(startnum, (int(endnum)+1)):
                button3[current_row].append(Button.inline(
                    str(i), data=f'ep:{i}:{data_split[2]}'))
                if i % 5 == 0:
                    button3.append([])
                    current_row = current_row + 1
            await event.edit(
                f'Choose Episode:',
                buttons=button3
            )

        elif 'etz:' in data:
            data_split = data.split(':')
            button3 = [[]]
            current_row = 0
            endnum = int(data_split[1])
            startnum = int(f'{endnum//100}01')
            for i in range(startnum, (int(endnum)+1)):
                button3[current_row].append(Button.inline(
                    str(i), data=f'ep:{i}:{data_split[2]}'))
                if i % 5 == 0:
                    button3.append([])
                    current_row = current_row + 1
            await event.edit(
                f'Choose Episode:',
                buttons=button3
            )
        
        elif 'ep:' in data:
            try:
                data_split = data.split(':')
                await send_download_link(event, data_split[2], data_split[1])
            except:
                pass
        elif 'spp:' in data:
            x = data.split(":")
            search_results = gogo.get_search_results(x[3])
            (names, ids) = format.format_search_results(search_results)
            for i in ids:
                if i[-25:] == x[2]:
                    id = i
                    break
            await send_download_link(event, id, x[1])
        
        elif 'dets:' in data:
            x = data.split(":")
            await send_details(event, x[1])

        elif 'split:' in data:
            await send_details(event, data)

    async def send_details(event, id):
        if 'split:' in id:
            split_id = id.split(":")
            x = gogo.get_search_results(split_id[1])
            (names, ids) = format.format_search_results(x)
            for i in ids:
                if i[-25:] == split_id[2]:
                    id = i
                    break

        search_details = gogo.get_anime_details(id)
        genre = search_details.get('genre')
        x = ''
        for i in genre:
            if i == "'" or i == "[" or i == "]":
                pass
            else:
                x = f'{x}{i}'
        await event.edit('Search Results:')
        try:
            await bot.send_message(
                event.sender_id,
                f"{search_details.get('title')}\nYear: {search_details.get('year')}\nStatus: {search_details.get('status')}\nGenre: {x}\nEpisodes: {search_details.get('episodes')}",
                file=search_details.get('image_url'),
                buttons=[Button.inline(
                    "Download", data=f"Download:{id}:{search_details.get('episodes')}")]
            )
        except:
            await bot.send_message(
                event.sender_id,
                f"{search_details.get('title')}\nYear: {search_details.get('year')}\nStatus: {search_details.get('status')}\nGenre: {x}\nEpisodes: {search_details.get('episodes')}",
                file=search_details.get('image_url'),
                buttons=[Button.inline(
                    "Download", data=f"longdl:{split_id[1]}:{id[-25:]}:{search_details.get('episodes')}")]
            )

    async def send_download_link(event, id, ep_num):
        links = gogo.get_episodes_link(animeid=id, episode_num=ep_num)
        result = format.format_download_results(links)
        await bot.send_message(
            event.sender_id,
            f"Download Links for episode {ep_num}\n{result}"
        )
except Exception as e:
    print(e)
