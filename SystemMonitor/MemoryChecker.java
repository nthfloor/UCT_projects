//thread class which retrieves and formats all memory information
//Nathan Floor
//FLRNAT001

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class MemoryChecker extends Thread{	
	private int totalMem;
	private int freeMem;
	private RefreshData refresher;
	
	public MemoryChecker(MainWindow gui){
		refresher = gui;
	}
	
	//reads in data
	public synchronized void fileReader(){		
		try{
			BufferedReader inputstream = new BufferedReader(new FileReader("/proc/meminfo"));
			String line = null;
			
			line = inputstream.readLine();
			totalMem = Integer.parseInt(line.substring(9,line.length()-2).trim());
			line = inputstream.readLine();
			freeMem = Integer.parseInt(line.substring(8,line.length()-2).trim());
			line = inputstream.readLine();
			freeMem = freeMem + Integer.parseInt(line.substring(8,line.length()-2).trim());
			line = inputstream.readLine();
			freeMem = freeMem + Integer.parseInt(line.substring(7,line.length()-2).trim());
			
			inputstream.close();
		}
		catch(FileNotFoundException e){}
		catch(IOException e){}		
	}
	
	//get methods
	public int getTotalMem(){
		return totalMem;
	}
	public int getFreeMem(){
		return freeMem;
	}
	
	//retrieves new data every 3 seconds
	public void run(){
		while(true){
			try{
				fileReader();
				refresher.updateMemory();
				sleep(3000);
			}
			catch(Exception e){}
		}		
	}
	
}
