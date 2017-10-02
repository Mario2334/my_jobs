import appJar

from jobs_scrape_wnh import mine

job_list = dict()
events = list()


def get_wnhjobs():
    a = mine()
    events.append('added')
    job_dict = a.run()
    print('event called')
    curr = ''
    if len(app.getAllListItems('wnhjobs')) > 10:
        app.clearListBox('wnhjobs')
        for i in job_dict.keys():
            k = job_list.popitem()

    if job_dict is not True:
        for i in job_dict.keys():
            job_list[i] = job_dict[i]

        keys = job_dict.keys()
        for i in keys:
            app.addListItem('wnhjobs', i)


def open_win(win):
    napp = appJar.gui()

    napp.setBg("DarkKhaki")
    napp.setGeometry(280, 400)

    curr_tAB = app.getTabbedFrameSelectedTab('Jobs')
    if curr_tAB == 'worknhire':
        get_item = app.getListItems('wnhjobs')
        get_list = app.getAllListItems('wnhjobs')
        job_details = job_list[get_item[0]]
    else:
        get_list = ['as', 'e', 'sde']

    job_desc = job_details[0][0]
    job_loc = job_details[1]
    no_of_bids = job_details[2][0]
    time_taken = job_details[2][1]
    skills = job_details[0][1]

    napp.startScrollPane(get_item[0])
    napp.addMessage(title=get_item[0], text=
    '''
                \t{0}\n\n\nDetails : {1}
                \n
                No of Bids : {2} \t Time required :{3} \n Skills : {4}
                '''.format(get_item[0], job_desc, no_of_bids, time_taken, skills
                           ))
    napp.addWebLink('Link', job_loc)
    napp.setStretch('both')
    napp.stopScrollPane()
    napp.go()


def check_stop():
    return app.yesNoBox('box', 'DO you want to exit')

if __name__=='__main__':

    app = appJar.gui('Hire me')

    app.startTabbedFrame('Jobs')
    app.startTab('worknhire')
    app.registerEvent(get_wnhjobs)
    app.setPollTime(time=10 * 60 * 1000)
    app.addListBox('wnhjobs')
    app.stopTab()
    app.startTab('upwork')
    app.addListBox('upjobs')
    app.stopTab()
    app.stopTabbedFrame()
    app.addButton('get data', open_win)

    app.setStopFunction(check_stop)
    app.go("200  500")
