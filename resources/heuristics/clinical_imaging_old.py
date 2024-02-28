# -*- coding: utf-8 -*-
import regex as re

diff_dic={
	'ADC':'ADC',
	'TRACEW':'TRACEW',
	'WEIGHTED TRACE':'TRACEW',
	'COLFA':'COLFA',
	'FA':'FA',
	'TENSOR':'TENSOR',
	'TENSOR_B0':'TENSOR',
}

def create_key(template, outtype=('nii.gz'), annotation_classes=None):
	if template is None or not template:
		raise ValueError('Template must be a valid format string')
	return (template, outtype, annotation_classes)

def get_unique(seqinfos, attr):
	"""Given a list of seqinfos, which must have come from a single study
	get specific attr, which must be unique across all of the entries
	If not -- fail!
	"""
	values = set(getattr(si, attr) for si in seqinfos)
#    assert (len(values) == 1)
	return values.pop()

def infotoids(seqinfos, outdir):
	
	subject = get_unique(seqinfos, 'example_dcm_file').split('_')[0]
	session = get_unique(seqinfos, 'example_dcm_file').split('_')[1]
	
	ids = {
	'locator': '',
	'session': session,
	'subject': subject,
	}
				
	return ids

# Utility:  Check a list of regexes for truthyness
def regex_search_label(regexes, label):
	if any(regex.search(label) for regex in regexes):
		out_list=[regex.search(label)[0] for regex in regexes if regex.search(label) is not None]
		return [x for x in out_list if x !='']
	else:
		return []

def is_diffusion_derived(label):
	regexes = [
		re.compile('ADC$', re.IGNORECASE),
		re.compile('TRACEW$', re.IGNORECASE),
		re.compile('WEIGHTED TRACE$', re.IGNORECASE),
		re.compile('COLFA$', re.IGNORECASE),
		re.compile('FA$', re.IGNORECASE),
		re.compile('TENSOR[_B0]*', re.IGNORECASE)
		]
	return regex_search_label(regexes, label)

def is_swi_derived(label):
	regexes = [
		re.compile('Mag$', re.IGNORECASE),
		re.compile('Pha$', re.IGNORECASE),
		re.compile('mIP$', re.IGNORECASE),
		]
	return regex_search_label(regexes, label)

def infotodict(seqinfo):
	"""Heuristic evaluator for determining which runs belong where

	allowed template fields - follow python string module:

	item: index within category
	subject: participant id
	seqitem: run number during scanning
	subindex: sub index within group
	"""
	
	#Anat
	t1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_T1w')
	t1w_acq = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_T1w')
	t2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_T2w')
	t1w_pd = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_PD')
	flair = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_FLAIR')
	flair_acq = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_FLAIR')
	
	#fmap
	fmap = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_run-{item:02d}_epi')
	fmap_acq = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_epi')

	#Diffusion
	dwi = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_dwi')
	dwi_acq = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_dwi')
	
	#CT
	ct = create_key('{bids_subject_session_dir}/ct/{bids_subject_session_prefix}_run-{item:02d}_ct')
	ct_acq = create_key('{bids_subject_session_dir}/ct/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_ct')
	ct_acq_desc = create_key('{bids_subject_session_dir}/ct/{bids_subject_session_prefix}_acq-{acq}_desc-{desc}_run-{item:02d}_ct')
	
	#pet
	pet = create_key('{bids_subject_session_dir}/pet/{bids_subject_session_prefix}_task-rest_run-{item:02d}_pet')
	pet_acq = create_key('{bids_subject_session_dir}/pet/{bids_subject_session_prefix}_task-rest_acq-{acq}_run-{item:02d}_pet')
	pet_task = create_key('{bids_subject_session_dir}/pet/{bids_subject_session_prefix}_task-{task}_acq-{acq}_run-{item:02d}_pet')

	#MIPS
	mips_sag = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SWI_rec-DIS2D_run-{item:02d}_sagMIP')
	mips_cor = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SWI_rec-DIS2D_run-{item:02d}_corMIP')
	mips_tra = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SWI_rec-DIS2D_run-{item:02d}_traMIP')

	#GRE (Susc3D)
	swi_gre = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SWI_run-{item:02d}_GRE')
	swi_gre_elec = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-Electrode_run-{item:02d}_GRE')
	mag_gre = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-mag_run-{item:02d}_GRE')
	phase_gre = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-phase_run-{item:02d}_GRE')

	#7T T2 SPACE
	spc_T2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-7T_run-{item:02d}_T2w')
	DIS2D_spc_T2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-7T_rec-DIS2D_run-{item:02d}_T2w')
	DIS3D_spc_T2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-7T_rec-DIS3D_run-{item:02d}_T2w')

	#7T MP2RAGE
	t1w_mprage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-7T_run-{item:02d}_T1w')
	t1map = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-7T_run-{item:02d}_T1map')

	info = {t1w:[],
			t1w_acq:[],
			t2w:[],
			t1w_pd:[],
			flair:[],
			flair_acq:[],
			fmap:[],
			fmap_acq:[],
			dwi:[],
			dwi_acq:[],
			ct:[],
			ct_acq:[],
			ct_acq_desc:[],
			pet:[],
			pet_acq:[],
			pet_task:[],
			mips_sag:[],
			mips_cor:[],
			mips_tra:[],
			swi_gre:[],
			swi_gre_elec:[],
			mag_gre:[],
			phase_gre:[],
			spc_T2w:[],
			DIS2D_spc_T2w:[],
			DIS3D_spc_T2w:[],
			t1w_mprage:[],
			t1map:[],
	}
	
	for idx, s in enumerate(seqinfo):
		if s.study_description is not None:

			#7T
			if 'neuroanalytics' in s.study_description.lower():

				if ('spc_T2' in s.series_description or 'T2w_SPC' in s.series_description or 'T2w_space' in s.series_description or 't2_space' in s.series_description or 't2_spc' in s.series_description or 'T2_spc' in s.series_description.strip() ): 					
					if ('ND' in (s.image_type[3].strip())):
						info[spc_T2w].append({'item': s.series_id})
					if ('DIS2D' in (s.image_type[3].strip())):
						info[DIS2D_spc_T2w].append({'item': s.series_id})
					if ('DIS3D' in (s.image_type[3].strip())):
						info[DIS3D_spc_T2w].append({'item': s.series_id})
				
				elif ('t1map' in s.series_description.strip().lower() or 't1_map' in s.series_description.strip().lower() or 't1_images' in s.series_description.strip().lower()):
					info[t1map].append({'item': s.series_id})

				elif ('mp2rage' in s.series_description.strip().lower() or 'mprage' in s.series_description.strip().lower()) and ('uni_images' in s.series_description.strip().lower()):
					info[t1w_mprage].append({'item': s.series_id})

			#MRI
			elif any(substring.upper() in s.study_description.upper() for substring in {'MR'}) and '_MPR_' not in s.series_description.upper():
				postop = False
				if 'SAR' in s.series_description.upper() or any(x in s.protocol_name.upper() for x in {'SAFE', 'STIMULATOR', 'STIM SAFE', 'POST', 'POST OP','POST-OP','DEPTH ELECTRODES'}):
					if not any(x.upper() in s.protocol_name.upper() for x in {'POST STROKE','GAD','+C','STEALTH POST','MPRAGE POST'}):
						postop = True
					
				if any(substring.upper() in s.series_description.upper() for substring in {'STEALTH', 'STEALTH BRAVO', 'AX STEALTH BRAVO','STEREO','STEREO-INCLUDE','1.5 MM ANATOMY','MPRAGE'}) and all(seq not in s.series_description.upper() for seq in ('FLAIR','FSPGR')):
					if 'MPGR' not in s.series_description.upper():
						if postop:
							if 'T2' in s.series_description.upper():
								info[t2w].append({'item': s.series_id, 'acq': 'Electrode'})
							else:
								info[t1w_acq].append({'item': s.series_id, 'acq': 'Electrode'})
						else:
							info[t1w].append({'item': s.series_id})
						
				elif 'EPI' in s.series_description.upper():
					if postop:
						info[fmap_acq].append({'item': s.series_id, 'acq': 'Electrode'})
					elif 'T2' in s.series_description.upper():
						info[fmap].append({'item': s.series_id})
				
				elif 'RAGE' in s.series_description.upper():
					if postop:
						info[t1w_acq].append({'item': s.series_id, 'acq': 'Electrode'})
					elif 'AX' in s.series_description.upper():
						info[t1w_acq].append({'item': s.series_id, 'acq': 'MPRAGE2D'})
					else:
						info[t1w_acq].append({'item': s.series_id, 'acq': 'MPRAGE'})

				elif 'FLAIR' in s.series_description.upper():
					if postop:
						info[flair_acq].append({'item': s.series_id, 'acq': 'Electrode'})
					elif 'AX' in s.series_description.upper():
						info[flair_acq].append({'item': s.series_id, 'acq': '2D'})
					else:
						info[flair].append({'item': s.series_id})

				elif any(substring.upper() in s.series_description.upper() for substring in {'IR_FSPGR', 'FSPGR','IR-FSPGR','SPGR'}):
					if postop:
						info[t1w_acq].append({'item': s.series_id, 'acq': 'Electrode'})
					else:
						if 'FSPGR' in s.series_description.upper():
							info[t1w_acq].append({'item': s.series_id, 'acq': 'FSPGR'})
						else:
							info[t1w_acq].append({'item': s.series_id, 'acq': 'SPGR'})
				
				elif any(substring.upper() in s.series_description.upper() for substring in {'SWI'}):
					if len(is_swi_derived(s.series_description))<1:
						if postop:
							info[swi_gre_elec].append({'item': s.series_id})
						else:
							info[swi_gre].append({'item': s.series_id})

				elif any(substring.upper() in s.series_description.upper() for substring in {'DWI', 'DTI', 'DIFFUSION','DWI-DTI'}):
					if len(is_diffusion_derived(s.series_description))>=1:
						srs_desc=None
						if '_' in s.series_description:	
							if any(s.series_description.split('_')[0]!=x for x in list(diff_dic)):
								if any(s.series_description.split('_')[-1]==x for x in list(diff_dic)):
									srs_desc=s.series_description.split('_')[-1]
							else:
								srs_desc=s.series_description.split('_')[0]
						else:
							srs_desc=s.series_description[0]
						
						if srs_desc is not None:
							str_derv=diff_dic[is_diffusion_derived(s.series_description)[0].upper()]
							info[dwi_acq].append({'item': s.series_id,'acq': str_derv if not postop else 'Electrode'+str_derv})
					else:
						if postop:
							info[dwi_acq].append({'item': s.series_id, 'acq': 'Electrode'})
						else:
							info[dwi].append({'item': s.series_id})

				elif any(substring.upper() in s.series_description.upper() for substring in {'AX', 'COR','SAG'}):
					orientation=''
					if '3D' not in s.series_description.upper():
						if ('AX' in s.series_description.upper()):
							orientation = 'Tra'
						elif ('COR' in s.series_description.upper()):
							orientation = 'Cor'
						elif ('SAG' in s.series_description.upper()):
							orientation = 'Sag'
					
					if postop:
						if any(substring.upper() in s.series_description.upper() for substring in {'T2', '2D'}):
							info[t2w].append({'item': s.series_id, 'acq': 'Electrode' + orientation})
						elif any(substring.upper() in s.series_description.upper() for substring in {'PD'}):
							info[t1w_pd].append({'item': s.series_id, 'acq': 'Electrode' + orientation})
						elif any(substring.upper() in s.series_description.upper() for substring in {'FLAIR'}):
							info[flair_acq].append({'item': s.series_id, 'acq': 'Electrode' + orientation})
						else:
							info[t1w_acq].append({'item': s.series_id, 'acq': 'Electrode' + orientation})
					else:
						if any(substring.upper() in s.series_description.upper() for substring in {'T2','2D'}):
							info[t2w].append({'item': s.series_id, 'acq': orientation})
						elif any(substring.upper() in s.series_description.upper() for substring in {'PD'}):
							info[t1w_pd].append({'item': s.series_id, 'acq': orientation})
						elif any(substring.upper() in s.series_description.upper() for substring in {'FLAIR'}):
							info[flair_acq].append({'item': s.series_id, 'acq': orientation})
						elif any(substring.upper() in s.series_description.upper() for substring in {'SSFSE'}):
							info[t1w_acq].append({'item': s.series_id, 'acq': 'SSFSE' + orientation})
			
			elif any(substring in s.study_description.upper() for substring in {'CT','HEAD','HEAD-STEREO'}) and 'SUMMARY' not in s.series_description.upper():
				electrode_list = {'OVER', 'UNDER', 'ELECTRODE', 'SD ELECTRODE', 'ROUTINE', 'F_U_HEAD', 'F/U_HEAD', 'ER_HEAD', 'POST OP','POSTOP','0.625 X 0.625','NO ANGLE','DEPTH ELECTRODES'}
				electrode_list_exact={'VOL. 0.5','STD STD 0.5'}
				ct_list_exclude={'AXIAL 2.500'}
				frame_list = {'STEROTACTIC', 'STEREOTACTIC','STEREOTACTIC FRAME', 'STEALTH', 'CTA_COW','AXIAL 1.200 CE','NC AXIAL 1.200','HEAD-STEREO','1.25 X 1.25',"1.25 X 1.25 AXIAL NO ANGLE"}
				frame_exclude={}
				
				if not all(x.upper() in s.series_description.upper() for x in ct_list_exclude):
					if (any(substring in ' '.join(s.protocol_name.upper().split()) for substring in electrode_list) or any(substring in s.series_description.upper() for substring in electrode_list) or any(substring == s.series_description.upper() for substring in electrode_list_exact))\
					and not any(x.upper() in ' '.join(s.series_description.upper().split()) for x in frame_list) and not any(x.upper() in ' '.join(s.protocol_name.upper().split()) for x in ['1.25 X 1.25']):
						if any(x.upper() in s.series_description.upper() for x in ('BONE','SEMAR')):
							info[ct_acq_desc].append({'item': s.series_id, 'acq': 'Electrode', 'desc':'BONE'})
						else:
							info[ct_acq].append({'item': s.series_id, 'acq': 'Electrode'})

					elif any(x.upper() in ' '.join(s.protocol_name.upper().split()) for x in frame_list) or any(substring.upper() in s.series_description.upper() for substring in frame_list) and not all(x.upper() in ' '.join(s.protocol_name.upper().split()) for x in frame_exclude):
						if any(x.upper() in s.series_description.upper() for x in ('BONE','SEMAR')):
							info[ct_acq_desc].append({'item': s.series_id, 'acq': 'Frame', 'desc':'BONE'})
						else:
							info[ct_acq].append({'item': s.series_id, 'acq': 'Frame'})

			elif any(substring.upper() in s.study_description.upper() for substring in {'PET'}) or any(substring.upper() in s.series_description.upper() for substring in {'PET CORR'}):
				if any(substring.upper() in s.series_description.upper() for substring in {'ITERATIVE','RECON','FBP','PET CORR','AC BRAIN DYN'}):
					if '3D_FBP' not in s.series_description.upper():
						info[pet].append({'item': s.series_id})
					
	return info
