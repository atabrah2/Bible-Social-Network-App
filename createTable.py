def createTable(topConnections, counts):
    html = '<table class="table table-hover"><thead><tr><th>Name</th><th>Connections</th></tr></thead><tbody>'
    idx = 0
    for connection in topConnections:
        html += '<tr data-toggle="modal" data-target="#myModal"><td>'
        html += connection[6:]
        html += '</td><td>'
        html += str(counts[idx])
        html += '</tr>'
        idx += 1
    html += '</tbody></table>'

    with open('table.html', 'w') as outfile:
        outfile.write(html)


counts = [  8,   9,   9,   9 , 10 , 12 , 12  ,13 , 14 , 14 , 14 , 15 , 15 , 15 , 15 , 16 , 16 , 17,
  18 , 18 , 18,  19  ,21,  23 , 24,  25 , 26 , 26  ,26 , 27  ,27 , 27,  28,  28,  28,  29,
  29  ,29,  29 , 30 , 30 , 31,  31 , 31,  32  ,38 , 38  ,40 , 51 ,129]
topConnections = ['/wiki/Josiah', '/wiki/Category:Judges', '/wiki/Jehu_(Prophet)', '/wiki/Job_(Person)', '/wiki/Jonathan_(Son_of_Gershom)', '/wiki/Joab', '/wiki/Jephthah', '/wiki/Category:Kings_of_Judah', '/wiki/Andrew', '/wiki/Aaron', '/wiki/James_(Son_of_Zebedee)', '/wiki/James_(Son_of_Alphaeus)', '/wiki/Matthew_(Apostle)', '/wiki/Category:Apostles', '/wiki/Philip_(Apostle)', '/wiki/Joseph_(Old_Testament)', '/wiki/John_the_Apostle', '/wiki/Barnabas', '/wiki/Tribes_of_Israel', '/wiki/Thomas', '/wiki/Matthias_(Apostle)', '/wiki/Paul', '/wiki/Category:Levites', '/wiki/Category:Early_Christians', '/wiki/Boaz', '/wiki/Peleg', '/wiki/Reu', '/wiki/Jared', '/wiki/Obed', '/wiki/Mahalalel', '/wiki/Arphaxad', '/wiki/Lamech_(Father_of_Noah)', '/wiki/Enosh', '/wiki/Enoch_(Jared%27s_son)', '/wiki/Jesse', '/wiki/Category:Old_Testament_Women', '/wiki/Cainan', '/wiki/Adam', '/wiki/Terah', '/wiki/Noah', '/wiki/Shelah', '/wiki/Methuselah', '/wiki/Jesus_Christ', '/wiki/Shem', '/wiki/Seth', '/wiki/Judah_(Patriarch)', '/wiki/Jacob', '/wiki/Abraham', '/wiki/David', '/wiki/Category:Old_Testament_Men']
print(list(reversed(topConnections)))
createTable(list(reversed(topConnections)), list(reversed(counts)))