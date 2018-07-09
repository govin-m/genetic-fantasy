import pandas as pd
import utils
import io

pd.options.display.max_columns=999

TARGET_URL="http://rotoguru1.com/cgi-bin/fyday.pl?game=dk&scsv=1&week=10&year=2011"

data = pd.DataFrame()

soup = utils.soup(TARGET_URL)
data = pd.read_csv(io.StringIO(soup.find("pre").text),sep=";")

data.to_csv("2011-10.csv")

