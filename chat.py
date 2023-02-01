from tkinter import *
import customtkinter
import openai
import os   #savefile
import pickle   #saveapifile 

#initiate app

root = customtkinter.CTk()
root.title("AI Bot")
root.geometry('600x750')
root.iconbitmap('ai_lt.ico') 

#set color scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

#submit to chatgpt

def speak():
	if chat_entry.get():
		# do something
		filename = "api_key"
		try:
			if os.path.isfile(filename):
				#open the file
				input_file=open(filename, 'rb')

				#load the data from the file into a variable
				stuff = pickle.load(input_file)

				#Query ChatGPT
				openai.api_key = stuff
				#create an instance
				openai.Model.list()
				#Define our query/Response
				response = openai.Completion.create(
					model="text-davinci-003",
					prompt=chat_entry.get(),
					temperature=0,
					max_tokens=250,
					top_p=1.0,
					frequency_penalty=0.0,
					presence_penalty=0.0,
					)
				my_text.insert(END, response["choices"][0]["text"].strip())
				my_text.insert(END, "\n\n")
				
			else:
				#create the file
				input_file = open(filename, 'wb')
				#close the file
				input_file.close()
				#error message - you need an api key
				my_text.insert(END, "\n\nYou need an API Key to talk with chatgpt. Get one here:\nhttps://platform.openai.com/account/api-keys")

		except Exception as e:
			my_text.insert(END, f"\n\n Error")
		
	else:
		my_text.insert(END, "\n\nHey! You Forgot to Type")
#clear the screen
def clear():
	#clear the main text box
	my_text.delete(1.0, END)
	#clear the query entry widget
	chat_entry.delete(0, END)
#Do api stuff
def key():

	#define our filename
	filename = "api_key"
	try:
		if os.path.isfile(filename):
			#open the file
			input_file=open(filename, 'rb')

			#load the data from the file into a variable
			stuff = pickle.load(input_file)

			#output stuff to our entry box
			api_entery.insert(END, stuff)
		else:
			#create the file
			input_file = open(filename, 'wb')
			#close the file
			input_file.close()
	except Exception as e:
		my_text.insert(END, f"\n\n Error")
	#Resize app
	root.geometry('600x750')
	#Reshow api frame
	api_frame.pack(pady=30)
#Save the API Key
def save_key():

	#define our filename
	filename = "api_key"
	try:
		#open file
		output_file = open(filename, 'wb')

		pickle.dump(api_entry.get(), output_file)
		#Delete the API KEy
		api_entry.delete(0, END)
		#hide api frame
		api_frame.pack_forget()
		#resize app smaller
		root.geometry('600x600')
	except Exception as e:
		my_text.insert(END, f"\n\n Error")
#create text frame
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

my_text = Text(text_frame, bg='#343638', width=65, bd=1, fg="#d6d6d6", relief="flat", wrap=WORD, 
	selectbackground='#1f538d')

my_text.grid(row=0, column=0)

#create scrollbar for text widget
text_scroll = customtkinter.CTkScrollbar(text_frame, command=my_text.yview)
text_scroll.grid(row=0, column=1, sticky="ns")
#add scrollbar to the text
my_text.configure(yscrollcommand=text_scroll.set)
#entry widget to type stuff to text to chatGPT
chat_entry = customtkinter.CTkEntry(root, 
	placeholder_text="Type something to ", #ChatGPT...
	width=535,
	height=50,
	border_width=2)
chat_entry.pack(pady=10)

#create button frame
button_frame = customtkinter.CTkFrame(root, fg_color="#242424")
button_frame.pack(pady=10)

#create submit button
submit_button = customtkinter.CTkButton(button_frame, text="Ask from AI",
	command=speak)
submit_button.grid(row=0, column=0, padx=25)
#create clear button
clear_button = customtkinter.CTkButton(button_frame, text="Clear Your response",
	command=clear)
clear_button.grid(row=0, column=1, padx=25)
#create api button
api_button = customtkinter.CTkButton(button_frame, text="Update API key",
	command=key)
api_button.grid(row=0, column=2, padx=25)

#Add API Key frame
api_frame = customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=30)

#Add API entry widget

api_entry = customtkinter.CTkEntry(api_frame, 
	placeholder_text="Enter your API Key",
	width=250, height=50, border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)

#Add API Button
api_save_button = customtkinter.CTkButton(api_frame,
	text="Save key",
	command=save_key)
api_save_button.grid(row=0, column=1, padx=10)

root.mainloop()