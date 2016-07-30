import argparse
from collections import defaultdict
import sys
import traceback

def wait_for_exit():
	input("Press Enter to exit")

class Configuration:
	def __init__(self, filename):
		self.stages = defaultdict(dict)
		cur_stage = "Start"
		cur_start = 0
		for l in open(filename, encoding="latin1"):
			splitLine = l.split("\t")
			try:
				self.stages[cur_stage][(int(splitLine[0])+cur_start, int(splitLine[1])+cur_start)] = []
			except:
				cur_stage = splitLine[0]
				cur_start = int(splitLine[1])
		self.windows = dict()
		for l in self.stages:
			for window in self.stages[l]:
				self.windows[window] = l

def test_window(window, time):
  if(window[0] < time < window[1]):
    return True
  return False

def parse_data(input, window, output_file):
  conf = Configuration(window)

  started = False
  output = defaultdict(list)
  phase = ""
  
  out = open(output_file, 'w')
  
  start = 0
  
  for l in open(input, encoding="latin1"):
    splitline = l.replace(",",".").split("\t")
    splitline[-1] = splitline[-1].strip()
    try:
      floats = [float(splitline[0])]
      if start == 0:
        start = floats[0]
      floats[0] -= start
    except:
      continue
	  
    for e in splitline:
      try:
        floats.append(float(e))
      except:
        floats.append(None)
    
    for w in conf.windows:
      if(test_window(w,floats[0])):
        conf.stages[conf.windows[w]][w].append(floats)

  results = list()
		
  for s in conf.stages:
    for w in conf.stages[s]:
      medians = list()
      i = 0
      f = 0
      if len(conf.stages[s][w]) == 0:
        continue
      for i in range(len(conf.stages[s][w][0])):
        i += 1
        try:
          temp_list = [l[i] for l in conf.stages[s][w] if l[i]]
          temp_list.sort()
          if(temp_list):
            medians.append(temp_list[len(temp_list)//2])
          else:
            medians.append(None)
        except:
          f += 1
          continue
      results.append([s,w,medians])
 
  results.sort(key=lambda t: t[1][0])
  for line in results:
    result_line = ""
    result_line += line[0]
    for e in line[2]:
      result_line += "\t" + str(e) 
    out.write(result_line + "\n")
  out.close()
	
	
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Automatic annotation of B2B data')
  parser.add_argument('-i', action="store", dest="input", help="Input file", default="input.tsv")
  parser.add_argument('-w', action="store", dest="window", help="Window definition file", default="windows.tsv")
  parser.add_argument('-o', action="store", dest="output", help="Output file", default="output.tsv")
  
  args = parser.parse_args()
  try:
    parsed_data = parse_data(args.input, args.window, args.output)
    print("Data parsed successfully.")
  except Exception as e:
    print(traceback.format_exc())
  wait_for_exit()