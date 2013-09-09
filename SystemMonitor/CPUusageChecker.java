//calculates the CPU usage of the system
//Nathan Floor
//FLRNAT001

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;

public class CPUusageChecker extends Thread{
	private ArrayList<Integer> oldCPUData;
	protected float percentage;
	protected RefreshData refresher;
	
	public CPUusageChecker(MainWindow gui){
		oldCPUData = fileReader();
		refresher = gui;
	}
	
	//reads in data
	public ArrayList<Integer> fileReader(){
		try{
			BufferedReader inputstream = new BufferedReader(new FileReader("/proc/stat"));
			String line = inputstream.readLine();
			
			line = line.substring(line.indexOf(" ")).trim();
			int user = Integer.parseInt(line.substring(0,line.indexOf(" ")).trim());
			line = line.substring(line.indexOf(" ")).trim();
			int nice = Integer.parseInt(line.substring(0,line.indexOf(" ")).trim());
			line = line.substring(line.indexOf(" ")).trim();
			int system = Integer.parseInt(line.substring(0,line.indexOf(" ")).trim());
			line = line.substring(line.indexOf(" ")).trim();
			int idle = Integer.parseInt(line.substring(0,line.indexOf(" ")).trim());
			
			ArrayList<Integer> temp = new ArrayList<Integer>();
			temp.add(user);
			temp.add(nice);
			temp.add(system);
			temp.add(idle);

			return temp;
		}
		catch(Exception e){return null;}
	}
	
	//updates data every second, and calculates CPU usage
	@Override
	public void run(){
		while(true){
			try{
				ArrayList<Integer> newCPUData = fileReader();
				
				float cpuUsage = (float)(newCPUData.get(0)-oldCPUData.get(0))+(newCPUData.get(1)-oldCPUData.get(1))+(newCPUData.get(2)-oldCPUData.get(2));
				float cpuMaxGiffies = (float)(newCPUData.get(0)-oldCPUData.get(0))+(newCPUData.get(1)-oldCPUData.get(1))+(newCPUData.get(2)-oldCPUData.get(2))+(newCPUData.get(3)-oldCPUData.get(3));
				percentage = cpuUsage/cpuMaxGiffies*100f;
				oldCPUData = newCPUData;
				refresher.updateCPUUsage(this);
				sleep(1000);
			}
			catch(Exception e){}
		}
	}
}
