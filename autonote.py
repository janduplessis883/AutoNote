# Import Libraries
import csv
from IPython.display import Javascript
from IPython.display import Markdown, display
from ipywidgets import Dropdown
from IPython.display import HTML, display
from importlib import reload
import pandas as pd


class AutoNote:
    def __init__(self, palette_no=5):
        self.color_1 = ""
        self.color_2 = ""
        self.color_3 = ""
        self.color_4 = ""
        self.color_5 = ""
        self.set_palette(palette_no)

        palette_preview = f"<table><tr><td style='background-color: #f7f7f7; height: 20px;'>☆ <B>AutoNote</B> ➞ </span></td><td style='background-color: #{self.color_1}; width: 30px; height: 20px;'>1</td><td style='background-color: #{self.color_2}; width: 30px; height: 20px;'>2</td><td style='background-color: #{self.color_3}; width: 30px; height: 20px;'>3</td><td style='background-color: #{self.color_4}; width: 30px; height: 20px;'>4</td><td style='background-color: #{self.color_5}; width: 30px; height: 20px;'>5</td><td style='background-color: #f7f7f7; height: 20px; font-size: 12px;'>setup( )</td></tr></table>"
        display(HTML(palette_preview))

        self.create_code_cell('# AutoNote Setup - Delete this cell once setup is complete\nan.setup()')
        # self.title('ML Project Title')
        # self.subhead1('Import Libraries')
        # self.import_lib()



    def set_palette(self, palette_no):
        if palette_no == 1:
            palette = ['e0e1dd','778da9','415a77','1b263b','0d1b2a']
        elif palette_no == 2:
            palette = ['f8c764','e08a61','da7b60','cf5f5f','c9505e']
        elif palette_no == 3:
            palette = ['52A9BE','547AA5','526685','4F5165','38393B']
        elif palette_no == 4:
            palette = ['eff6e0','aec3b0','598392','124559','01161e']
        elif palette_no == 5:
            palette = ['ced4da','6c757d','495057','343a40','212529']
        elif palette_no == 6:
            palette = ['C9CDC6','4C8B96','457E88','3F737C','396971']
        elif palette_no == 7:
            palette = ['FBB13C','C5A64D','8E9A5E','218380','58586B']
        elif palette_no == 8:
            palette = ['F5E3E0','E8B4BC','D282A6','A0647E','6E4555']

        self.color_1 = palette[0]
        self.color_2 = palette[1]
        self.color_3 = palette[2]
        self.color_4 = palette[3]
        self.color_5 = palette[4]


    def setup(self):  # -------------------------------------------------
        options = """<table>
                    <tr>
                        <td style='background-color: #f7f7f7; text-align:left; vertical-align:top;'>☆ <B>AutoNote</B> Setup ➞ </td>
                        <td style='background-color: #f7f7f7; text-align:left;'>
                        1. <B>Themed Markdown only</B> ➞ Load themed markdown cells, duplicate and use your own notebook.<br>
                        2. <B>Theme + Initial Data Exploration</B> ➞ Load themed markdown cells, with initial data exploration code cells.<br>
                        3. <B>Themed Dataset Preparation</B> ➞ Themed Pre-processing code cells for ML dataset preparation.<br>
                        4. <B>Dataset Preparation Code</B> ➞ Pre-processing code cells for ML dataset preparation.<br>
                        <a href="#" style="color: #343a40; text-decoration: none;" onmouseover="this.style.color='#495057';" onmouseout="this.style.color='#6c757d';" onvisited="this.style.color='#6c757d';">Documentation</a>
                        </td>
                    </tr>
                    </table>
                    """
        display(HTML(options))
        setupno = int(input("Select setup (1-4): "))

        if setupno == 2:
            title = input("Project Title: ")
            goal = input("Define the problem, ML approach, the data, and the relevant metrics: ")
            self.title(title, goal)
            self.import_lib()

        elif setupno == 3:
            self.pre_process()

        elif setupno == 4:
            pass

        elif setupno == 1:
            self.theme_only()

    def highlight_cells(val):
        color1 = '#{self.color_1}' if val > 0.6 else color1
        color2 = '#{self.color_2}' if val > 0.8 else color2
        return 'background-color: %s' % color


    def create_code_cell(self, code):  # -------------------------------------------------
        display(Javascript("""
            var code = `{}`;
            var cell = Jupyter.notebook.insert_cell_above('code');
            cell.set_text(code);
        """.format(code)))

    def create_markdown_cell(self,text):
        display(Javascript("""
            var text = `{}`;
            var cell = Jupyter.notebook.insert_cell_above('markdown');
            cell.set_text(text);
        """.format(text)))

    # -HTML Title-----------------------------------------------------------------------------
    def title(self, info, goal='Define the problem: Identify the type of ML model needed, the data available, and the relevant metrics'):
        output = f"<div class='alert' style='background-color: #{self.color_5}; color: #{self.color_1}; padding:26px 26px; border-radius:15px; font-size:40px;'><B>{info}</B></div><div style='margin:8px 26px; color:#{self.color_5}; font-size:18px;'>✭ {goal}</div><BR><BR>"
        display(Javascript("""
            var text = `{}`;
            var cell = Jupyter.notebook.insert_cell_above('markdown');
            cell.set_text(text);
        """.format(output)))

    # -HTML Subheading-----------------------------------------------------------------------------
    def subhead1(self, info, txt=''):
        if txt != '':
            output = f"<div class='alert' style='background-color: #{self.color_4}; color:#{self.color_1}; padding:10px 26px; border-radius:10px; font-size:20px;'><b>{info}</B></div><div class='plain' style='color:#{self.color_4}; padding: 6px 26px; font-size:16px;'><B></B>{txt}</div>"
        else:
            output = f"<div class='alert' style='background-color: #{self.color_4}; color:#{self.color_1}; padding:10px 26px; border-radius:10px; font-size:20px;'><b>{info}</B></div>"


        display(Javascript("""
        var text = `{}`;
        var cell = Jupyter.notebook.insert_cell_above('markdown');
        cell.set_text(text);
        """.format(output)))

    # -HTML Subheading-----------------------------------------------------------------------------
    def subhead2(self, info, txt=''):
        if txt != '':
            output = f"<div class='alert' style='background-color: #{self.color_3}; color:#{self.color_1}; padding:10px 26px; border-radius:10px; font-size:20px;'><b>{info}</B></div><div class='plain' style='color:#{self.color_3}; padding: 6px 26px; font-size:16px;'><B></B>{txt}</div>"
        else:
            output = f"<div class='alert' style='background-color: #{self.color_3}; color:#{self.color_1}; padding:10px 26px; border-radius:10px; font-size:20px;'><b>{info}</B></div>"

        display(Javascript("""
        var text = `{}`;
        var cell = Jupyter.notebook.insert_cell_above('markdown');
        cell.set_text(text);
        """.format(output)))

    # -HTML Subheading-----------------------------------------------------------------------------
    def subhead3(self, info, txt=''):
        if txt != '':
            output = f"<div class='alert' style='background-color: #{self.color_2}; color:#{self.color_1}; padding:10px 26px; border-radius:10px; font-size: 20px;'><b>{info}</b></div><div class='plain' style='color:#{self.color_2}; padding: 6px 26px; font-size:16px;'><B></B>{txt}</div>"
        else:
            output = f"<div class='alert' style='background-color: #{self.color_2}; color:#{self.color_1}; padding:10px 26px; border-radius:10px; font-size: 20px;'><b>{info}</b></div>"
        display(Javascript("""
        var text = `{}`;
        var cell = Jupyter.notebook.insert_cell_above('markdown');
        cell.set_text(text);
        """.format(output)))


    # -HTML Info-----------------------------------------------------------------------------
    def html_info(self, info):
        output = f"<div style='color:#{self.color_4}; font-size: 18px; margin: 6px 8px;'><B>☞  {info}</div>"
        display(Javascript("""
        var text = `{}`;
        var cell = Jupyter.notebook.insert_cell_above('markdown');
        cell.set_text(text);
        """.format(output)))

    # -Light Line -----------------------------------------------------------------------------
    def h_line(self):
        output = f"<div class='alert' style='background-color: #{self.color_1}; color:white; padding:1px 4px; border-radius:6px;'></div><BR>"
        display(Javascript("""
        var text = `{}`;
        var cell = Jupyter.notebook.insert_cell_above('markdown');
        cell.set_text(text);
        """.format(output)))

    def all_headings(self):
        self.title("Project Title")
        self.subhead1('Sub Head 1', 'Substring here with additional infomration about this section')
        self.subhead2('Sub Head 2')
        self.subhead3('Sub Head 3')
        self.html_info('HTML Info Tab')
        self.h_line()




    def split_bp(self, df, column, delimiter, new_column_1, new_column_2):
        # Split the values in the column by the delimiter
        df[new_column_1], df[new_column_2] = df[column].str.split(delimiter, 1).str
        df[new_column_1] = pd.to_numeric(df[new_column_1], errors='coerce')
        df[new_column_2] = pd.to_numeric(df[new_column_2], errors='coerce')
        df = df
        # Drop the original column
        return df


    # --NLP Basic Text Cleaning  LOWER SLICE NUMBERS PUNCTUATION REMOVER --------------
    def nlp_basic_cleaning(self, sentence):
        import string

        sentence = ''.join(char for char in sentence if not char.isdigit())

        for punctuation in string.punctuation:
            sentence = sentence.replace(punctuation, '')

        sentence = sentence.lower()
        sentence = sentence.strip()
        return sentence

    # --Load Libraries --------------
    def import_lib(self):
        self.subhead1('Loading Libraries + Read data', 'Loading basic DS Libraries. Read csv (dataset) to pandas DataFrame.')
        self.create_code_cell("# Importing Libraries\nimport matplotlib.pyplot as plt\nimport pandas as pd\nimport numpy as np\nimport seaborn as sns\n\n# Hi-resolution Plots and Matplotlib inline\n%config InlineBackend.figure_format = 'retina'\n%matplotlib inline")
        self.create_code_cell("# Load dataset / csv file\ndata = pd.read_csv('../jan-datasets/FILE.csv')\ndata.head()")
        self.subhead1('Initial Data Exploration', 'DataFrame shape, info( ) and describe( )')
        self.create_code_cell("data.shape")
        self.create_code_cell("data.info()")
        self.create_code_cell("data.describe().T.round(3)")
        self.subhead1('Correlation + Exploratory Plots', 'Further exploration of data correlation.')
        self.create_code_cell("data.corr().round(3)")
        self.html_info('Plotting: <code>sns.pairplot</code>')
        self.create_code_cell("# sns.pairplot to explore numberic data correlation & outliers.\nsns.pairplot(data)")
        self.html_info('Plotting: </B>Correlation & Heatmap')
        self.create_code_cell("data.corr().round(3)")
        self.create_code_cell("# sns.heatmap cmap options flare (red/purple), crest (blue), other, other\nsns.heatmap(data.corr(), annot=True, annot_kws={'size': 9}, fmt='.2f', cmap='flare')")
        self.h_line()

    def pre_process(self):
        self.html_info("Data Preparation</B> - Duplicates, Missing Data, Outliers, Feature Scalling, Dataset balancing, Encoding")
        self.subhead2('Duplicates', 'Remove duplicate data entries.')
        self.create_code_cell("data.duplicated().sum() # Compute the number of duplicated rows")
        self.create_code_cell("data = data.drop_duplicates() # Remove duplicates\nlen(data) # Check new number of rows")
        self.subhead2('Missing Values', 'Dealing with missing values in your dataset, made easy!')
        self.create_code_cell("# Counting the number of NaN for each column\ndata.isnull().sum().sort_values(ascending=False)")
        self.html_info("sklearn.preprocessing.StandardScaler")
        self.create_code_cell("")
        self.html_info("sklearn.preprocessing.MinMaxScaler")
        self.create_code_cell("")
        self.html_info("sklearn.preprocessing.RobustScaler")
        self.create_code_cell("")
        self.subhead2('Outliers', 'Identify and managing Outliers.')
        self.create_code_cell("")
        self.subhead2('Feature Scaling', 'Standardizing, normilization, MinMax Scaling, Robust Scaling, Scaling in practice with Scikit Learn')
        self.create_code_cell("")
        self.subhead2('Dataset Balancing', 'Oversampling of minority class, Undersampling of majority class.')
        self.create_code_cell("")
        self.subhead2('Encoding', 'Transforming non-numerical data into an equivalent numerical form.')
        self.html_info("sklearn.preprocessing.OrdinalEncoder")
        self.create_code_cell("")
        self.html_info("sklearn.preprocessing.OneHotEncoder")
        self.create_code_cell("")
        self.html_info("sklearn.preprocessing.LabelEncoder")
        self.create_code_cell("")
        self.h_line()




    # - Project Frame -----------------------------------------------------------------------------
    def theme_only(self):
        self.title("Project Title", "Project description: Define the problem, ML approach, the data, and the relevant metrics.")
        self.subhead1('Sub Heading 1', "Sub Heading 1 description.")
        self.subhead2('Sub Heading 2', "Sub Heading 2 description.")
        self.subhead3('Sub Heading 3', "Sub Heading 3 description.")
        self.html_info('Information markdown cell')
        self.h_line()

    # - NLP - Basic and Advance Sentence Cleaning  -------------------------------------------------
    # 🖥️ Example of calling the clena function
    # cleaned_document = data["sentence"].apply(cleaning)
    # cleaned_document.head()

    def cleaning(sentence):

        import string
        import nltk
        from nltk.tokenize import word_tokenize
        from nltk.corpus import stopwords
        from nltk.stem import WordNetLemmatizer

        # Basic cleaning
        sentence = sentence.strip() ## remove whitespaces
        sentence = sentence.lower() ## lowercase
        sentence = ''.join(char for char in sentence if not char.isdigit()) ## remove numbers

        # Advanced cleaning
        for punctuation in string.punctuation:
            sentence = sentence.replace(punctuation, '') ## remove punctuation

        tokenized_sentence = word_tokenize(sentence) ## tokenize
        stop_words = set(stopwords.words('english')) ## define stopwords

        tokenized_sentence_cleaned = [ ## remove stopwords
            w for w in tokenized_sentence if not w in stop_words
        ]

        lemmatized_v = [
            WordNetLemmatizer().lemmatize(word, pos = "v")
            for word in tokenized_sentence_cleaned
        ]

        lemmatized_n = [
            WordNetLemmatizer().lemmatize(word, pos = "n")
            for word in tokenized_sentence_cleaned
        ]

        cleaned_sentence = ' '.join(word for word in lemmatized_v)
        cleaned_sentence = ' '.join(word for word in lemmatized_n)

        applying_function = "# Sentences needs to be in a dataframe = data with column heading = sentence\ncleaned_document = data['sentence'].apply(cleaning)\ncleaned_document.head()"
        create_code_cell(applying_function)

        return cleaned_sentence


# import pandas as pd

# df = pd.DataFrame({'A': [0.5, 0.7, 0.8, 0.6], 'B': [0.4, 0.6, 0.9, 0.7]})

# def highlight_cells(val):
#    def highlight_cells(val):
    # color = 'green' if val > 0.6 else 'white'
    # color = 'red' if val > 0.8 else color
    # return 'background-color: %s' % color

# df.style.applymap(highlight_cells)

# import matplotlib.colors as mcolors

# my_cmap = mcolors.LinearSegmentedColormap.from_list('my_colormap',
#                                                     ['green', 'yellow', 'red'])

# plt.imshow(data, cmap=my_cmap)
# plt.colorbar()
# plt.show()
