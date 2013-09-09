//thread class to retrieve info on all process running on system
//Nathan Floor
//FLRNAT001

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

import javax.swing.table.DefaultTableModel;

public class ProcessChecker extends Thread{
	private int numRunningProcs = 0;
	private int numZomProcs = 0;
	private int maxProcesses;
	private int numProcs;
	private ArrayList<Process> allProcesses = new ArrayList<Process>();
	private RefreshData refresher;
	
	public ProcessChecker(MainWindow gui){
		refresher = gui;
	}
	
	//reads in data
	public synchronized void fileReader(){
		try{
			BufferedReader inputstream = new BufferedReader(new FileReader("/proc/stat"));
			String line = null;
			
			//retrieve max number of processes possibly running on system
			while(true){				
				line = inputstream.readLine();
				if(line.substring(0, 9).equals("processes")){					
					maxProcesses = Integer.parseInt(line.substring(10));
					break;
				}			
			}//end while
			inputstream.close();
			getProcessInfo();
		}
		catch(FileNotFoundException e){}
		catch(IOException e){}
	}
	
	//retrieve all info on each process currently running
	public synchronized void getProcessInfo(){		
		int counter = 1;	
		allProcesses = new ArrayList<Process>();
		try{			
			File myfile = null;
			while(counter <= maxProcesses){	
				myfile = new File("/proc/"+counter+"/status");	
				if(myfile.canRead()){
					Process temp = new Process(myfile);	
					
					//combine processes and their memory, who have the same name
					if(allProcesses.contains(temp))
						allProcesses.get(allProcesses.indexOf(temp)).combineProcess(temp);
					else
						allProcesses.add(temp);
				}
				myfile = null;
				counter++;
			}//end while
		}
		catch(Exception e){}		
		numProcs = allProcesses.size();
	}//end of getProcessInfo
	
	//returns table model of processes for the JTable in the GUI
	public synchronized DefaultTableModel getTableModel(){
		DefaultTableModel myModel = new DefaultTableModel();
		myModel.setColumnCount(4);
		myModel.setColumnIdentifiers(new String[] {"Name","Pid","State","Memory in Kb"});
		
		Collections.sort(allProcesses);
		Object[] data = new Object[4];
		
		numRunningProcs = 0;
		numZomProcs = 0;
		for(Process p : allProcesses){
			if(p.state.equals("R (running)"))
				numRunningProcs++;
			if(p.state.equals("Z (zombie)"))
				numZomProcs++;
			data[0] = p.name;
			data[1] = p.PID;
			data[2] = p.state;
			data[3] = p.memory;
			
			myModel.addRow(data);
		}		
		return myModel;
	}

	public ArrayList<Process> getProcesses(){
		ArrayList<Process> temp = new ArrayList<Process>();
		for(Process p : allProcesses)
			temp.add(p);
		
		return temp;
	}

	//get methods
	public int getNumProcs(){
		return numProcs;
	}
	public int getNumRunningProcs(){
		return numRunningProcs;
	}
	public int getZombieProcs(){
		return numZomProcs;
	}

	//reads in new data every 3 seconds
	public void run(){		
		while(true){			
			try{
				fileReader();
				refresher.updateProcess();
				sleep(3000);					
			}
			catch(Exception e){}			
		}		
	}
}//end of class
