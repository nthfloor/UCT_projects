//class containing all the data on each process
//Nathan Floor
//FLRNAT001

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

public class Process implements Comparable<Process>{
	protected String name;
	protected String state;
	protected int PID;
	protected int memory;

	//reads in data and formats it appropriatly
	public Process(File myfile){		
		int count = 0;
		String line = null;

		try{
			BufferedReader inputstream = new BufferedReader(new FileReader(myfile));
			while(count < 15){

				line = inputstream.readLine();
				if(count == 0){
					name = line.substring(5).trim();
				}
				else if(count == 1){
					state = line.substring(6).trim(); 
				}
				else if(count == 3){
					PID = Integer.parseInt(line.substring(4).trim());
				}					              
				else if(count == 14){
					if(line.substring(0,5).equals("VmRSS"))							
						memory = Integer.parseInt(line.substring(6,line.length()-2).trim());
					else
						memory = 0;
					break;
				}
				count++;
			}
			inputstream.close();
		}
		catch(Exception e){}	
	}

	public String toString(){
		return name + " \t" + PID + " \t" + state + " \t" + memory;
	}

	//combines memory of all processes with the same name
	public void combineProcess(Process p){
		if(p.state.equals("R (running)"))
			this.state = p.state;
		else if(p.state.equals("Z (zombie)")&&(this.state.equals("S (sleeping)")))
				this.state = p.state;
		
		this.memory += p.memory;
	}
	
	//used to check if the supplied process is contained in the ArrayList of processes
	public boolean equals(Object p){
		if(p instanceof Process){
			if(((Process)p).name.equals(this.name))
				return true;
			else
				return false;
		}
		else
			return false;
	}
	
	//used in ProcessChecker.getTableModel() to sort the ArrayList according to memory
	@Override
	public int compareTo(Process target) {
		if(target.memory < this.memory)
			return -1;
		else if(target.memory > this.memory)
			return 1;
		else		
			return 0;
	}
}
