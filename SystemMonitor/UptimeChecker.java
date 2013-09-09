//class that extends Thread in order to continuously retrieve new data on the uptime
//Nathan Floor
//FLRNAT001

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;


public class UptimeChecker extends Thread{	
	private String uptime;
	private RefreshData refresher;
	
	public UptimeChecker(MainWindow gui){
		refresher = gui;
	}
	
	//reads in data from uptime file found in /proc directory
	public synchronized void fileReader(){		
		try{
			BufferedReader inputstream = new BufferedReader(new FileReader("/proc/uptime"));
			String line = inputstream.readLine();				
			double temp = Double.parseDouble(line.substring(0,line.indexOf(" ")).trim());
			int numHours = (int)(temp/60)/60;
			int numDays = 0;
			
			//formats data to display meaningful information
			while(numHours > 24){
				numHours = numHours-24;
				numDays++;
			}	
			String days;
			if(numDays == 0)
				days = "";
			else if(numDays < 2)
				days = numDays + " day, ";
			else
				days = numDays+ " days, ";
			
			int numMinutes = (int)(((temp/60)/60 - numDays*24 - numHours)*60);
			String minutes;
			if(numMinutes < 10)
				minutes = "0"+numMinutes;
			else
				minutes = numMinutes+"";
				
			int numSeconds = (int)((((temp/60)/60 - numDays*24 - numHours)*60 - numMinutes)*60);
			String seconds;
			if(numSeconds < 10)
				seconds = "0"+numSeconds;
			else
				seconds = ""+numSeconds;
			uptime = days+numHours+":"+minutes+":"+seconds;			
			inputstream.close();
		}
		catch(FileNotFoundException e){}
		catch(IOException e){}
	}
	
	//get method
	public String getUptime(){
		return uptime;
	}
	
	//thread continuously runs in background, updating data every second
	public void run(){
		while(true){
			try{
				fileReader();
				refresher.updateUptime();
				sleep(1000);
			}
			catch(Exception e){}
		}
	}
}
