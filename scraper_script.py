import scrapers.treehugger as treehugger
import scrapers.zerowastehome as zerowastehome

def run_scrapers():
    '''
    Runs all invidual scrapers and returns them in one list
    Scrapers: treehugger, zerowastehome
    '''
    th = treehugger.scrape_treehugger()
    zwh = zerowastehome.scrape_zerowastehome()
    
    return th + zwh

if __name__ == "__main__":
    print(run_scrapers())
