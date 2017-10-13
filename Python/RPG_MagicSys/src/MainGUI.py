'''
Created on Oct 6, 2017

@author: Haunspergers
'''


import json
from FrameScrollbar import FrameScrollbar
from tkinter import Tk, IntVar, StringVar, Menu, Frame, Label, ttk, Text, Button, \
    Checkbutton, messagebox, Canvas, Scrollbar, Entry
from tkinter.constants import *

from SpellMakerGUI import OpenGUI
from tkinter.filedialog import askopenfilename


data={}
data["stats_filename"]="data/stats.json"
data["elements_filename"]="data/elements.json"
data["spellAttributes_filename"]="data/spell_attributes.json"
data["wizardSpells_filename"]="data/wizard_spells.json"
data["classes_filename"]="data/classes.json"
data["runes_filename"]="data/runes.json"

with open(data["stats_filename"], 'r') as f:
    data["stats"] = json.load(f)
with open(data["classes_filename"], 'r') as f:
    data["classes"] = json.load(f)       
with open(data["runes_filename"], 'r') as f:
    data["runes"] = json.load(f)
with open(data["elements_filename"], 'r') as f:
    data["elements"] = json.load(f)
with open(data["spellAttributes_filename"], 'r') as f:
    data["spellAttributes"] = json.load(f)
with open(data["wizardSpells_filename"], 'r') as f:
    data["wizardSpells"] = json.load(f)

class MainGUI:
    def __init__(self,player_filename=""):
        
        
        ############### load data and save settings
        self.save_on = True
        
        if not player_filename:
            player_filename = "data/character_template.json"
            self.save_on = False
        
        self.player_filename = player_filename
        
        with open(player_filename, 'r') as f:
            self.playerdata = json.load(f)
            
        self.player_class_data = data["classes"][self.playerdata["class"]]
        
        
            ##########
        
        self.root = Tk()
        
        
        

        
        
        ### variables
        
        self.levelvar = IntVar()
        self.levelvar.set(self.playerdata["level"])
        
        self.namevar = StringVar()
        self.namevar.set(self.playerdata["name"])
        
        self.goldvar = IntVar()
        self.goldvar.set(self.playerdata["gold"])
        
        self.background_text = self.playerdata["background"]
        
        self.journal_text = self.playerdata["journal"]
        
        ##############################
        #add widgets
        self.GUIMenu()
        
        self.GUIHeader()
        
        self.GUIBody()
        
        
        
        ##############################
        
        
        ### configure root
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1,minsize=400)
        self.root.grid_columnconfigure(0, weight=1,minsize=400)
        
        
        self.root.title("RPG Leveler")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
        
        
        
    ##############################
    #   Constructor functions    #
    ##############################
        
        
        
        ### add menu
    def GUIMenu(self):
        self.menubar = Menu(self.root)
        
        self.fileMenu = Menu(self.menubar, tearoff=0)
        self.fileMenu.add_command(label="Open", command=self.open_file)
        self.fileMenu.add_command(label="Save", command=self.save)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)
        
        self.spellMenu = Menu(self.menubar, tearoff=0)
        self.spellMenu.add_command(label="Add Spell", command=OpenGUI)
        self.spellMenu.add_command(label="Edit Spell", command=self.hello)
        self.menubar.add_cascade(label="Spells", menu=self.spellMenu)
        
        self.itemMenu = Menu(self.menubar, tearoff=0)
        self.itemMenu.add_command(label="Add Item", command=self.hello)
        self.itemMenu.add_command(label="Edit Item", command=self.hello)
        self.menubar.add_cascade(label="Items", menu=self.itemMenu)
        
        self.root.config(menu=self.menubar)
        
        
        
        
        
        
        
        ### add header
        
        
    def GUIHeader(self):
        
        self.header = Frame(self.root,pady=5)
        
        
        self.header_name = Label(self.header,text="Name: ")
        self.header_namevar = Label(self.header,textvariable=self.namevar)
        
        self.header_level = Label(self.header,text="Level: ")
        self.header_levelvar = Label(self.header,textvariable=self.levelvar)
        
        self.header_gold = Label(self.header,text="Gold: ")
        self.header_goldvar = Label(self.header,textvariable=self.goldvar)
        
        
        
        self.header.grid(row=0,column=0,sticky="NSEW")
        
        self.header_name.grid(row=0,column=0,sticky="NSEW")
        self.header_namevar.grid(row=0,column=1,sticky="NSEW")
        
        self.header_level.grid(row=0,column=3,sticky="NSEW")
        self.header_levelvar.grid(row=0,column=4,sticky="NSEW")
        
        self.header_gold.grid(row=0,column=6,sticky="NSEW")
        self.header_goldvar.grid(row=0,column=7,sticky="NSEW")
        
        
        
        ### configure header grid
        
        self.header.grid_columnconfigure(2,minsize=30,weight=2)
        self.header.grid_columnconfigure(5,minsize=30,weight=2)
        self.header.grid_columnconfigure(8,weight=5)
        
        
        
    def GUIBody(self):
        
        #notebook
        self.body = ttk.Notebook()
        
        self.tabAbilities = Frame(self.root)
        self.tabClass = Frame(self.root)
        self.tabSkills = Frame(self.root)
        self.tabItems = Frame(self.root)
        self.tabBackground = Frame(self.root)
        self.tabJournal = Frame(self.root)
        
        ###########################
        #add tabs
        self.GUIAbilitiesTab()
        self.GUIBackgroundTab()
        self.GUIClassTab()
        self.GUIItemsTab()
        self.GUIJournalTab()
        self.GUIOverviewTab()
        self.GUISkillsTab()
        #
        ###########################
        self.body.add(self.tabAbilities,text="Abilities")
        self.body.add(self.tabClass,text=self.player_class_data["tab_name"])
        self.body.add(self.tabSkills,text="Skills")
        self.body.add(self.tabItems,text="Items")
        self.body.add(self.tabBackground,text="Background")
        self.body.add(self.tabJournal,text="Journal")
        

        self.body.grid(row=1,column=0,sticky="NSEW")
     
     
     
        
    ##################################
    #            tabs                #
    ##################################
        
        

    def GUIBackgroundTab(self):
        self.background_box = Text(self.tabBackground,width=10,height=10,font="TkFixedFont",wrap=WORD)
        self.background_box.insert(END,self.background_text)
        self.background_box.grid(row=0,column=0,sticky="NSEW")
        self.tabBackground.grid_rowconfigure(0, weight=1)
        self.tabBackground.grid_columnconfigure(0, weight=1)


    

    def GUIJournalTab(self):
        self.journal_box = Text(self.tabJournal,width=10,height=10,font="TkFixedFont",wrap=WORD)
        self.journal_box.insert(END,self.journal_text)
        self.journal_box.grid(row=0,column=0,sticky="NSEW")
        self.tabJournal.grid_rowconfigure(0, weight=1)
        self.tabJournal.grid_columnconfigure(0, weight=1)
        
        
        
    def GUIAbilitiesTab(self):
        
        
        self.Attributes = {}
        self.i=0
        self.Abilities_pointsLeftvar = IntVar()
        self.Abilities_pointsLeftvar.set(self.playerdata["points"]["attributes"])
        
        #header
        self.tabAbilities_abil = Frame(self.tabAbilities,padx=10,pady=10)
        self.tabAbilities_pointsLeft = Label(self.tabAbilities,text="Points Left:")
        self.tabAbilities_pointsLeftvar = Label(self.tabAbilities,textvariable=self.Abilities_pointsLeftvar)
        
        
        
        #attributes
        for attribute in self.playerdata["stats"]["attributes"]:
                #print(attribute)
                self.Attributes[attribute] = {}
                self.Attributes[attribute]["value"] = IntVar()
                self.Attributes[attribute]["value"].set(self.playerdata["stats"]["attributes"][attribute])
                
                self.Attributes[attribute]["button+"] = Button(self.tabAbilities_abil,text="+",command=lambda attribute=attribute: self.change_attribute(attribute,1))
                self.Attributes[attribute]["button-"] = Button(self.tabAbilities_abil,text="-",command=lambda attribute=attribute: self.change_attribute(attribute,-1))
                self.Attributes[attribute]["valueLabel"] = Label(self.tabAbilities_abil,textvariable=self.Attributes[attribute]["value"],font=("Ariel", 25))
                self.Attributes[attribute]["atributeLabel"] = Label(self.tabAbilities_abil,text=attribute.upper()+" ",font=("Ariel", 25))
                self.Attributes[attribute]["spacerLabel"] = Label(self.tabAbilities_abil,text="",height=1)
                
                self.Attributes[attribute]["atributeLabel"].grid(row=self.i,column=0,sticky="NSEW",rowspan=2)
                self.Attributes[attribute]["button-"].grid(row=self.i+1,column=4,sticky="NSEW")
                self.Attributes[attribute]["valueLabel"].grid(row=self.i,column=2,sticky="NSEW",rowspan=2)
                self.Attributes[attribute]["button+"].grid(row=self.i,column=4,sticky="NSEW")
                self.Attributes[attribute]["spacerLabel"].grid(row=self.i+2,column=3,sticky="NSEW")
                
                self.i+=3
        
        self.tabAbilities_pointsLeftvar.grid(row=0,column=2)
        self.tabAbilities_pointsLeft.grid(row=0,column=1)
        self.tabAbilities_abil.grid(row=1,column=0)


        
    def GUISkillsTab(self):

        self.Skills = {}
        self.sk_x=0
        self.sk_y=0
        
        
        #attributes
        for skill in data["stats"]["skills"]:
            
            #print(skill)
            self.Skills[skill["name"]] = {}
            
            self.Skills[skill["name"]]["frame"] = Frame(self.tabSkills,relief="sunken",bd=1)
            
            self.Skills[skill["name"]]["isTrained"] = IntVar()
            self.Skills[skill["name"]]["isTrained"].set(self.playerdata["stats"]["skills"][skill["name"]])
            
            self.Skills[skill["name"]]["value"] = IntVar()
            self.Skills[skill["name"]]["value"].set((self.Attributes[skill["base"]]["value"].get()-10)//2+self.Skills[skill["name"]]["isTrained"].get()*2)
            
            #print (self.Skills[skill["name"]]["value"].get())
            
            self.Skills[skill["name"]]["check"] = Checkbutton(self.Skills[skill["name"]]["frame"],variable=self.Skills[skill["name"]]["isTrained"],state=DISABLED,command=lambda skill=skill: print(skill))
            self.Skills[skill["name"]]["valueLabel"] = Label(self.Skills[skill["name"]]["frame"],textvariable=self.Skills[skill["name"]]["value"],font=("Ariel", 12))
            self.Skills[skill["name"]]["atributeLabel"] = Label(self.Skills[skill["name"]]["frame"],text=skill["name"]+" ",font=("Ariel", 12))
            
            
            self.Skills[skill["name"]]["frame"].grid(row=self.sk_y,column=self.sk_x,sticky="we")
            
            self.Skills[skill["name"]]["check"].pack(side="left")
            self.Skills[skill["name"]]["atributeLabel"].pack(side="left")
            self.Skills[skill["name"]]["valueLabel"].pack(side="right")
            
            
            self.sk_x+=1
            if self.sk_x > 1:
                self.sk_y+=1
                self.sk_x=0
        


        ######## Items
    def GUIItemsTab(self):
        
        
        self.itemSFrame = FrameScrollbar(self.tabItems)
            
        self.itemid=0
        self.Items = []
        
        for item in self.playerdata["items"]:
            
            self.Items.append({})
            self.Items[self.itemid]["id"]=self.itemid
            self.Items[self.itemid]["frame"] = Frame(self.itemSFrame.frame,relief=RIDGE,bg="grey",padx=1,pady=1)
            self.Items[self.itemid]["button_delete"] = Button(self.Items[self.itemid]["frame"],text="X",fg="white",bg="red",command=lambda Itemid=self.itemid:delItem(Itemid))
            self.Items[self.itemid]["name"] = Entry(self.Items[self.itemid]["frame"])
            self.Items[self.itemid]["name"].insert(END, item["name"])
            self.Items[self.itemid]["description"] = Text(self.Items[self.itemid]["frame"],width=10,height=5,wrap=WORD)
            self.Items[self.itemid]["description"].insert(END,item["description"])
            
            self.Items[self.itemid]["name"].grid(row=0,column=0)
            self.Items[self.itemid]["button_delete"].grid(row=0,column=0,sticky="E")
            self.Items[self.itemid]["description"].grid(row=1,column=0,sticky="NSEW")
            self.Items[self.itemid]["frame"].grid(padx=10,pady=10,sticky="EW")
            
            self.Items[self.itemid]["frame"].grid_columnconfigure(0, weight=1)
            
            
            
            self.itemid+=1
            
        def addItem():
            item={}
            item["id"]=self.itemid
            item["frame"] = Frame(self.itemSFrame.frame,relief=RIDGE,bg="grey",padx=1,pady=1)
            item["button_delete"] = Button(item["frame"],text="X",fg="white",bg="red",command=lambda Itemid=self.itemid:delItem(Itemid))
            item["name"] = Entry(item["frame"])
            item["description"] = Text(item["frame"],width=10,height=5,wrap=WORD)
            item["name"].grid(row=0,column=0)
            item["button_delete"].grid(row=0,column=0,sticky="E")
            item["description"].grid(row=1,column=0,sticky="NSEW")
            item["frame"].grid(padx=20,pady=10,sticky="EW")
            item["frame"].grid_columnconfigure(0, weight=1)
            
            self.itemSFrame.frame.update_idletasks()
            self.itemSFrame.onCanvasConfigure(None)
            
            
            
            self.Items.append(item)
            
            self.itemid+=1
            
    
            
        def delItem(Itemid):
            item=""
            index=0
            for item in self.Items:
                if item["id"]==Itemid:
                    index=self.Items.index(item)
                    break
                else:
                    item=""
            if item:
                self.Items[index]["frame"].grid_remove()
                self.Items.remove(item)
                
            self.itemSFrame.frame.update_idletasks()
            self.itemSFrame.onCanvasConfigure(None)
        
        self.addItemButton = Button(self.itemSFrame.canvas_frame,text="+",bg="grey",command=addItem).place(rely=1.0, relx=0.0, x=5, y=-5, anchor="sw")
            
        ######## Class
    def GUIClassTab(self):
        pass

        ######## Overview
    def GUIOverviewTab(self):
        pass






        
        
        
        
        
        
        
    
    #######################################
    #            functions                #
    #######################################
        


    def hello(self):
        pass
    
    
    
    def change_attribute(self,attribute,amount):
        if amount>0:
            if self.Abilities_pointsLeftvar.get()>0:
                self.Attributes[attribute]["value"].set(self.Attributes[attribute]["value"].get()+amount)
                self.Abilities_pointsLeftvar.set(self.Abilities_pointsLeftvar.get()-1)
        else:
            if self.Attributes[attribute]["value"].get()>self.playerdata["stats"]["base_attributes"][attribute]:
                self.Attributes[attribute]["value"].set(self.Attributes[attribute]["value"].get()+amount)
                self.Abilities_pointsLeftvar.set(self.Abilities_pointsLeftvar.get()+1)
        self.updateSkills()
    
    
    def on_close(self):
        if self.save_on and messagebox.askyesno("RPG","Do you want to save changes?"):
            self.save()
        self.root.destroy()
    
    
    
    def save(self):
        if self.save_on:
            
            for attribute in self.playerdata["stats"]["attributes"]:
                self.playerdata["stats"]["attributes"][attribute] = self.Attributes[attribute]["value"].get()
                self.playerdata["items"]=[]
            for item in self.Items:
                ditem = {}
                ditem["name"]=item["name"].get()
                ditem["description"]=item["description"].get(1.0,END)[:-1]
                self.playerdata["items"].append(ditem)
            
            
            self.playerdata["level"] = self.levelvar.get()
            self.playerdata["name"] = self.namevar.get()
            self.playerdata["gold"] = self.goldvar.get() 
            self.playerdata["background"] = self.background_box.get(1.0,END)[:-1]
            self.playerdata["journal"] =  self.journal_box.get(1.0,END)[:-1]
            self.playerdata["points"]["attributes"] = self.Abilities_pointsLeftvar.get()
            
            print(self.playerdata)
            
            with open(self.player_filename, 'w') as player_file:
                json.dump(self.playerdata, player_file, indent=4)
        
    def updateSkills(self):
        for skill in data["stats"]["skills"]:
            self.Skills[skill["name"]]["value"].set((self.Attributes[skill["base"]]["value"].get()-10)//2+self.Skills[skill["name"]]["isTrained"].get()*2)
        
    def open_file(self):
        p_fn = openFileName()
        if p_fn:
            self.root.destroy()
            openGUI(p_fn)

def openFileName():
    temp=Tk()
    temp.withdraw()
    temp.overrideredirect(1)
    player_filename=askopenfilename(filetypes=[("Player files (.rpgplayer)","*.rpgplayer"),("JSON files (.json)","*.json"),("All",".*")])
    temp.deiconify()
    temp.destroy()
    return player_filename



def openGUI(player_filename=openFileName()):
    GUI = MainGUI(player_filename)
    del GUI



openGUI()