'''
Created on Oct 7, 2017

@author: Haunspergers
'''

import json
from tkinter import *



class SpellMakerGUI:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
        self.spells_file="data/custom_spells.json"
        
        
        with open(self.spells_file, 'r') as spellsfile:
            self.spelldata = json.load(spellsfile)
            
        self.root = Tk()
        
        self.root.title("Spell Maker")
        
        
        self.NumbersOnly = (self.root.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        
        
        
        self.insert_example = Label(self.root,text="(Insert multiple items as comma separated list)").grid(row=0,column=0,columnspan=2)
        
        self.spell_name_text = Label(self.root,text="Name: ")
        self.spell_name_text.grid(row=1,column=0)
        self.spell_name_input = Entry(self.root)
        self.spell_name_input.grid(row=1,column=1,sticky="W")
        
        self.spell_description_text = Label(self.root,text="Description: ")
        self.spell_description_text.grid(row=2,column=0)
        self.spell_description_input = Text(self.root,width=15,height=7,wrap=WORD)
        self.spell_description_input.grid(row=2,column=1,sticky="NSEW")
        
        self.spell_elements_text = Label(self.root,text="Elements: \n(comma separated)")
        self.spell_elements_text.grid(row=3,column=0)
        self.spell_elements_input = Entry(self.root)
        self.spell_elements_input.grid(row=3,column=1,sticky="W")
        
        self.spell_shape_text = Label(self.root,text="Shape:")
        self.spell_shape_text.grid(row=4,column=0)
        self.spell_shape_input = Entry(self.root)
        self.spell_shape_input.grid(row=4,column=1,sticky="W")
        
        self.spell_level_text = Label(self.root,text="Level:")
        self.spell_level_text.grid(row=5,column=0)
        self.spell_level_input = Entry(self.root, validate = 'key', validatecommand = self.NumbersOnly)
        self.spell_level_input.grid(row=5,column=1,sticky="W")
        
        self.spell_mana_text = Label(self.root,text="Mana:")
        self.spell_mana_text.grid(row=6,column=0)
        self.spell_mana_input = Entry(self.root, validate = 'key', validatecommand = self.NumbersOnly)
        self.spell_mana_input.grid(row=6,column=1,sticky="W")
        
        self.spell_damage_text = Label(self.root,text="Damage: ")
        self.spell_damage_text.grid(row=7,column=0)
        self.spell_damage_input = Entry(self.root, validate = 'key', validatecommand = self.NumbersOnly)
        self.spell_damage_input.grid(row=7,column=1,sticky="W")
        
        self.spell_components_text = Label(self.root,text="Components: \n(comma separated)")
        self.spell_components_text.grid(row=8,column=0)
        self.spell_components_input = Entry(self.root)
        self.spell_components_input.grid(row=8,column=1,sticky="W")
        
        #####################################
        
        self.buttons = Frame(self.root,pady=20).grid(columnspan=2,rowspan=5,sticky="NSEW")
        
        self.button_Add = Button(self.buttons,text="Add",command=self.save).grid(row=11,column=0)
        self.button_Cancel = Button(self.buttons,text="Cancel",command=lambda: self.root.destroy()).grid(row=11,column=1)
        
        #####################################
        
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        
        #####################################
            
        self.root.mainloop()
        
    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if(action=='1'):
            if text in '0123456789.-+':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True
        
    def save(self):
        self.spell={}
        self.spell["name"]=self.spell_name_input.get()
        self.spell["description"]=self.spell_description_input.get(1.0,END)[:-1]
        self.spell["elements"]=self.spell_elements_input.get().split(",")
        self.spell["shape"]=self.spell_shape_input.get()
        self.spell["level"]=int(self.spell_level_input.get())
        self.spell["mana"]=int(self.spell_mana_input.get())
        if self.spell_components_input.get():
            self.spell["components"]=self.spell_components_input.get().split(",")
        if self.spell_damage_input.get():
            self.spell["damage"]=self.spell_damage_input.get()
        
        
        self.spelldata["spells"].append(self.spell)
        
        with open(self.spells_file, 'w') as spellsfile:
            json.dump(self.spelldata, spellsfile, indent=4)
        self.root.destroy()
        
def OpenGUI():
    GUI = SpellMakerGUI()