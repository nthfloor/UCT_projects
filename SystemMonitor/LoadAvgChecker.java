//class that handles the load average data
//Nathan Floor
//FLRNAT001

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class LoadAvgChecker extends Thread{	
	private String loadavg;
	private RefreshData refresher;
	
	public LoadAvgChecker(MainWindow gui){
		refresher = gui;
	}
	
	//reads in data
	public void fileReader(){
		try{
			BufferedReader inputstream = new BufferedReader(new FileReader("/proc/loadavg"));
			String line = inputstream.readLine();			
			loadavg = line.substring(0,15).trim();			
			inputstream.close();
		}
		catch(FileNotFoundException e){}
		catch(IOException e){}
	}
	
	//get method
	public String getLoadAvg(){
		return loadavg;
	}

	//updates data every 3 seconds
	public void run(){
		while(true){
			try{
				fileReader();
				refresher.updateLoadAvg();
				sleep(3000);
			}
			catch(Exception e){}
		}
	}
}
