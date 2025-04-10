import h5py
import numpy as np

def data_loader(filepath, camera='output' ,load_interferograms=False):
    profile = []
    profile_r = []
    phase_r = []
    interferograms = []
    
    with h5py.File(filepath, 'r') as hf:
        number_of_passages = np.array(hf['number_of_passages'])
        for i in range(1, number_of_passages + 1):
            passage = 'passage_'+str(i)
            dataset = hf[passage][camera]
            profile.append(dataset["profile"][:][0])
            profile_r.append(dataset["profile_r"][:][0])
            phase_r.append(dataset["phase_r"][:][0])
            
            if load_interferograms:
                interferograms.append(dataset['interferogram'][:][0])
            
    return np.array(profile), np.array(profile_r), np.array(phase_r), np.array(interferograms)

def get_number_of_passages(filepath):
    with h5py.File(filepath, 'a') as hf:
        number_of_passages = np.array(hf['number_of_passages'])
    return number_of_passages
    
def data_saver(filepath, passage_number,
               output_profile, output_profile_r, output_phase_r, output_interferogram=0,
               next_mask_AM=0, next_mask_SLM=0,
               input_profile=0, input_profile_r=0, input_phase_r=0, input_interferogram=0):
    
    
            
    with h5py.File(filepath, 'a') as hf:
        try:
            number_of_passages = np.array(hf['number_of_passages'])
            if number_of_passages < passage_number:
                del hf['number_of_passages']
                hf['number_of_passages'] = passage_number
        except:
            try:
                del hf['number_of_passages']
                hf['number_of_passages']=1
            except:
                hf['number_of_passages']=passage_number
            

        number_of_passages = hf['number_of_passages']
        passage = 'passage_'+str(passage_number)
        try:
            hf.create_group(passage)
        except:
            del hf[passage]
            hf.create_group(passage)
        
        grp = hf[passage]
        
        ###########input group##########
        grp.create_group("input")
        input_group = grp['input']
        input_group.create_dataset("profile",  data=[input_profile])
        input_group.create_dataset("profile_r",  data=[input_profile_r])
        input_group.create_dataset("phase_r",  data=[input_phase_r])
        input_group.create_dataset("input_interferogram",  data=[input_interferogram])
        
        ###########output group##########
        grp.create_group("output")
        output_group = grp['output']
        output_group.create_dataset("profile",  data=[output_profile])
        output_group.create_dataset("profile_r",  data=[output_profile_r])
        output_group.create_dataset("phase_r",  data=[output_phase_r])
        output_group.create_dataset("output_interferogram",  data=[output_interferogram])
        
        ##########masks group###########
        grp.create_group("next_masks")
        masks_group = grp['next_masks']
        masks_group.create_dataset("next_mask_AMP",  data=[next_mask_AM])
        masks_group.create_dataset("next_mask_SLM",  data=[next_mask_SLM])