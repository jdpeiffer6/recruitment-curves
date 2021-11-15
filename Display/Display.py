import numpy as np

class jdplot():
    
    def plot_new_data(self,data_to_plot):
        for i in range(len(data_to_plot[0])):
            print(data_to_plot[0][i],end="\r")

    def log_new_data(self,data_to_log):
        if self.count < 19947:
            l = len(data_to_log[0])
            self.log[0,self.count:(self.count+l)] = data_to_log[0]
            self.log[1,self.count:(self.count+l)] = data_to_log[1]
            self.count = self.count + l +1
        else:
            np.save('C:\\Users\\QTM\\Documents\\Delsys\\jd\\output\\myfile.npy',self.log)
            print("Done")


    def initiate(self,nplot):
        for i in range(nplot):
            print('S'+str(i),end ="\t")
        print('\n')

        self.log = np.empty([2,20000])
        self.count = 0