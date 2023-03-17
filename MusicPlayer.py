#Nick Brown CSC202
#Project 2
#Week of 3/1/2021
#Music Player


#Ideas to add:############################################################################################################################################################################
#Add ability to create personalized playlists
#Add two dropdown menus, one where you select song name, artist, and album, and another that that lets you choose from a list based on previous answer


import pygame
from tkinter import *
from PIL import ImageTk
import random


#Creates node added to Linked List and holds song information###########################################################
class DoublyLinkedListNode:

    def __init__(self, myPrev, name, artist, album, artwork, artworkResize, song, myNext):
        #Construct a new Linked List Node
        self.prev = myPrev
        self.name = name
        self.artist = artist
        self.album = album
        self.artwork = artwork
        self.artworkResize = artworkResize
        self.song = song
        self.next = myNext
        return
        
#Circular Doubly Linked List used for song order#############################################################################################
class DoublyLinkedList:

    def __init__(self):
        #Construct a new LinkedList. The first node and last node are the same. Size is 0
        self.firstNode = None 
        self.lastNode = self.firstNode
        self.size = 0
        return

    def addToRear(self, name, artist, album, artwork, artworkResize, song):
        #Add a node to the list
        node = DoublyLinkedListNode(None, name, artist, album, artwork, artworkResize, song, None)

        if self.firstNode == None: 
            self.firstNode = node
            self.lastNode = node
        else:
            node.prev = self.lastNode
            self.lastNode.next = node
            self.lastNode = node
        self.lastNode.next = self.firstNode
        self.firstNode.prev = self.lastNode

        self.size += 1

        return

    def removeFromFront(self):
        #Remove a node from the front of the list

        if self.size == 0:
            print ("Linked List is empty")
            frontData = None
        else:
            currentNode = self.firstNode
            frontData = currentNode.data

            # This is the case where we have only one node in the list
            if currentNode.next == None:
                self.firstNode = None 
                self.lastNode = self.firstNode
                self.size = self.size - 1
            else:

                # Here there are more than one nodes in the list
                currentNode = currentNode.next
                self.firstNode = currentNode
                currentNode.prev = self.lastNode
                self.size = self.size - 1

        return frontData

    def addToFront(self, name, artist, album, artwork, artworkResize, song):
        #Push a node onto the stack
        node = DoublyLinkedListNode(None, name, artist, album, artwork, artworkResize, song, None)

        if self.firstNode == None: 
            self.firstNode = node
            self.lastNode = node
        else:
            node.next = self.firstNode
            self.firstNode.prev = node
            self.firstNode = node
        self.firstNode.prev = self.lastNode

        self.size += 1

        return

    def removeFromRear(self):
        if self.size == 0:
            print ("Linked List is empty")
            rearData = None
        else:
            currentNode = self.firstNode
            rearData = currentNode.data

            # This is the case where we have only one node in the list
            if self.size == 1:
                self.firstNode = None 
                self.lastNode = self.firstNode
            else:
                currentNode = self.lastNode.prev
                self.lastNode = currentNode
                currentNode.next = self.firstNode
                
            self.size = self.size - 1

        return rearData

    def __str__(self):
        currentNode =  self.firstNode

        for i in range(self.size):
            print (currentNode.data)
            currentNode = currentNode.next

        return "Reached end of list.\n"
###############################################################################################



#Song Commands
def playsong():
    global playing, paused
    playing = True
    paused = False
    pygame.mixer.music.play()

def pausesong():
    global paused, playing
    if playing:
        if paused:
            pygame.mixer.music.unpause()
            paused = False
        else:
            pygame.mixer.music.pause()
            paused = True

def nextsong():
    global currentsong, paused
    currentsong = currentsong.next
    loadsong(currentsong)
    playsong()

def previoussong():
    global currentsong
    currentsong = currentsong.prev
    loadsong(currentsong)
    playsong()
    
def stopsong():
    global playing, paused
    pygame.mixer.music.stop()
    playing = False
    paused = False

#Loads the song and info about to be used##################################################################################################
def loadsong(song):
    global picture, currentsong
    currentsong = song
    canvas.delete("cover", "info")
    picture = ImageTk.PhotoImage(file = song.artwork)
    pygame.mixer.music.load(currentsong.song)
    #Creates the various information displayed when the song is loaded
    canvas.create_image(300, 300, image = picture, tags = 'cover')
    canvas.create_text(300, 615, text = currentsong.name, font = "Times 20 bold", tags = "info")
    canvas.create_text(300, 640, text = currentsong.artist, font = "Times 10", tags = "info")
    canvas.create_text(300, 660, text = currentsong.album, font = "Times 10", tags = "info")

#functions used by search button###########################################################################################################
def search():
    global albumcount
    searchinput = searchVar.get()
    #Starts search with first node
    searchsong = Library.firstNode
    albumcount = 0
    find(searchinput, searchsong)
    return

def find(searchinput, song):
    global searchedFrame, searchImageList, counter, albumcount, Album
    #When something is searched, this destroys the old frame containing search info
    if song == Library.firstNode:
        counter = 0
        searchedFrame.destroy()
        searchedFrame = Frame(root)
        searchedFrame.grid(row = 0, rowspan = 10, column = 1)
        searchImageList = []
    #Finds the songs searched for, when the image is clicked, the song will play ################### 
    if searchinput == song.name or searchinput == song.artist or searchinput == song.album:
        #If you look up an album name and there are multiple songs from the album, It will give you an option to play that album independently
        if searchinput == song.album:
            if albumcount == 0:
                #Creates Album
                Album = DoublyLinkedList()
                x = Library.firstNode
                for i in range(Library.size):
                    if x.album == song.album:
                        Album.addToRear(x.name, x.artist, x.album, x.artwork, x.artworkResize, x.song)
                        albumcount += 1
                    x = x.next
                #If the album has multiple songs, it will be offered
                if albumcount > 1:
                    #Results for Album
                    image = ImageTk.PhotoImage(file = song.artworkResize)
                    searchImageList.append(image)
                    Button(searchedFrame, image = searchImageList[counter], command = lambda: loadsong(Album.firstNode)).grid(row = counter, column = 0)#
                    text = song.artist + "\n" + song.album
                    Label(searchedFrame, text = text).grid(row = counter, column = 1)
                    counter += 1
                #If the album only has one song, the album will be reverted to a placeholder
                else:
                    Album = Library
        #Results for individual songs             
        image = ImageTk.PhotoImage(file = song.artworkResize)
        searchImageList.append(image)
        Button(searchedFrame, image = searchImageList[counter], command = lambda: loadsong(song)).grid(row = counter, column = 0)
        text = song.name + "\n" + song.artist + "\n" + song.album
        Label(searchedFrame, text = text).grid(row = counter, column = 1)
        counter += 1
    #Search does not end until the last node is reached, ensuring no matching song is missed
    if song != Library.lastNode:
        find(searchinput, song.next)

#Clears the search bar and frame    *EXTRA*
def clear():
    searchVar.set("")
    search()


#Sets up ability to shuffle the music###############    *EXTRA*    ##########################################################################################################################

#extracts song data from Library or album and creates a shuffled library or album###################################################################################

def shuffle(Music):
    global currentsong
    ShuffledLibrary = DoublyLinkedList()
    song = Music.firstNode
    songlist = []
    for i in range(Music.size):
        songlist.append(song)
        song = song.next
    checklist = []
    for i in range(len(songlist)):
        shuffdatalist = []
        x = random.randint(0, len(songlist)-1)
        #Makes sure songs do not get repeated, although could slow process
        while x in checklist:
            x = random.randint(0, len(songlist)-1)
        checklist.append(x)
        ShuffledLibrary.addToRear(songlist[x].name, songlist[x].artist, songlist[x].album, songlist[x].artwork, songlist[x].artworkResize, songlist[x].song)
    currentsong = ShuffledLibrary.firstNode
    loadsong(currentsong)
    playsong()

#extracts song data from text file and adds them to Library in order############################################################################################################
def createlibrary():
    global Library
    Library = DoublyLinkedList()
    songlist = open("songlist.txt", "r")
    songfiles = songlist.readlines()
    songlist.close()
    for i in range(len(songfiles)):
        datalist = []
        file = songfiles[i]
        songinfolist = file.split(",")
        for i in range(6):
            if i == 3:
                datalist.append("Images/" + songinfolist[i].strip())
            elif i == 4:
                datalist.append("Resized Images/" + songinfolist[i].strip())
            elif i == 5:
                datalist.append("Music/" + songinfolist[i].strip())
            else:
                datalist.append(songinfolist[i].strip())
        Library.addToRear(datalist[0], datalist[1], datalist[2], datalist[3], datalist[4], datalist[5])
    currentsong = Library.firstNode
    loadsong(currentsong)
##################################################################################################################################################

#Starts audio player
pygame.mixer.init()

#Sets up the GUI###########################################################################################
paused = False
playing = False
root = Tk()
root.title('Music Player')

#creates area for song data
canvas = Canvas(root, height = 670, width = 600)
canvas.grid(row = 0, column = 0)

#uses function to set up and load music, sets album equal to library as a placeholder
createlibrary()
Album = Library

#Creates an are for the song control buttons
buttonFrame = Frame(root)
buttonFrame.grid(row = 1, column = 0)

#Creates an area for buttons that change music order/content, shuffle, albums, etc.
alternateOrderFrame = Frame(root)
alternateOrderFrame.grid(row = 2, column = 0)

#Creates area for search bar, as well as an area for search results
searchFrame = Frame(root)
searchFrame.grid(row = 3, column = 0)
searchedFrame = Frame(root)
searchedFrame.grid(rowspan = 10, column = 1)
searchImageList = []
counter = 0

#Creates various GUI elements###########################################################################
searchVar = StringVar()
playButton = Button(buttonFrame, text='Play', command = playsong)
pauseButton = Button(buttonFrame, text='Pause', command = pausesong)
prevButton = Button(buttonFrame, text='Previous', command = previoussong)
nextButton = Button(buttonFrame, text='Next', command = nextsong)
stopButton = Button(buttonFrame, text='Stop', command = stopsong)

shuffleButton = Button(alternateOrderFrame, text='Shuffle Library', command = lambda: shuffle(Library))
resetButton = Button(alternateOrderFrame, text='Reset Load Order', command = createlibrary)
shuffleAlbumButton = Button(alternateOrderFrame, text='Shuffle Album', command = lambda: shuffle(Album))

searchEntry = Entry(searchFrame, textvariable = searchVar)
searchButton = Button(searchFrame, text = "Search", command = search)
clearSearchButton = Button(searchFrame, text = "Clear", command = clear)

#Configures and places GUI elements###########################################################################
searchEntry.config(width = 60)
prevButton.grid(row = 0, column = 0)
pauseButton.grid(row = 0, column = 1)
playButton.grid(row = 0, column = 2)
stopButton.grid(row = 0, column = 3)
nextButton.grid(row = 0, column = 4)

shuffleButton.grid(row = 0, column = 0)
resetButton.grid(row = 0, column = 1)
shuffleAlbumButton.grid(row = 0, column = 2)

searchEntry.grid(row = 0, column = 0)
searchButton.grid(row = 0, column = 1)
clearSearchButton.grid(row = 0, column = 2)


root.mainloop()
