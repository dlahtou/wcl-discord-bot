from random import sample, choice

def pick(command):
    strings = command.split(' ')

    # handle bad commands
    num_to_pick = strings[0][5:]
    if num_to_pick.isdigit():
        num_to_pick = int(num_to_pick)
    else:
        return('You have to put a number after /pick! I don\'t understand the command!')
    
    pick_options = strings[1:]
    
    if num_to_pick >= len(pick_options):
        return('I can\'t pick {} out of {} options! Take them all!'.format(num_to_pick, len(pick_options)))
    
    # make picks
    picked_options = sample(pick_options, num_to_pick)

    # format reply
    if len(picked_options) == 1:
        formatted_pick_list = picked_options[0]
    elif len(picked_options) == 2:
        formatted_pick_list = ' and '.join(picked_options)
    else:
        picked_options[-1] = 'and ' + picked_options[-1]
        formatted_pick_list = ', '.join(picked_options)

    REPLY_FORMAT_STRINGS = [
        'Hmmmm.... How about {}?',
        'Red Rover, Red Rover, let {} come over!',
        'I pick {}!',
        'Let\'s go with {}'
    ]

    print('Returning picks!')
    return(choice(REPLY_FORMAT_STRINGS).format(formatted_pick_list))
