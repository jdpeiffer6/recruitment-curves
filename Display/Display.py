import numpy as np

class jdplot():

    def log_new_data(self,data_to_log):
        if self.count < 19947:
            l = len(data_to_log[0])
            self.log[0,self.count:(self.count+l)] = data_to_log[0]
            self.log[1,self.count:(self.count+l)] = data_to_log[1]
            self.count = self.count + l
            # TODO: see if there is an error with the every other sample
        else:
            np.save('output\\myfile.npy',self.log)
            print("Done")


    def initiate(self,nplot):
        for i in range(nplot):
            print('S'+str(i),end ="\t")
        print('\n')

        self.log = np.empty([2,20000])
        self.count = 0