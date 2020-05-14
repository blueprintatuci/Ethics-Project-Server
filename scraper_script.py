import scrapers.treehugger as treehugger
import scrapers.zerowastehome as zerowastehome

def run_scrapers(recent_articles):
    '''
    Input: recent_articles is a dictionary of site names whose values are the most recent article put in the table
    Runs all invidual scrapers and returns them in one list
    Scrapers: treehugger, zerowastehome
    '''
    th = treehugger.scrape_treehugger(recent_articles['treehugger'])
    zwh = zerowastehome.scrape_zerowastehome(recent_articles['zerowastehome'])
        
    return th + zwh

if __name__ == "__main__":
    print(run_scrapers())
