#!/usr/bin/python
import argparse
import ioutil as i_o

def main():

    ### arguments.
    # set arguments.
    parser = argparse.ArgumentParser(description='Get versions of software deployed on Docker container.')
    parser.add_argument('--infile', metavar='<program_usage_or_version_file>', type=str, required=True)
    args = parser.parse_args()
    # get arguments.
    infile = args.infile

    # get software output lines
    io = i_o.IOUtil()
    output_lines = io.get_results(infile)
    # get program name
    program_name = infile.split('/')[-1].split('_')[0]
    version = ''
    if (program_name == 'annovar' or
        program_name == 'bwa' or
        program_name == 'samtools' or
        program_name == 'sailfish'):
        version = io.parse_multiple_lines(output_lines, program_name)
    elif (program_name == 'bowtie' or
          program_name == 'bowtie2' or
          program_name == 'cufflinks' or
          program_name == 'express' or
          program_name == 'gatk' or
          program_name == 'hisat2' or
          program_name == 'kallisto' or
          program_name == 'last' or
          program_name == 'picard' or
          program_name == 'salmon' or
          program_name == 'star' or
          program_name == 'stringtie' or
          program_name == 'tophat2' or
          program_name == 'trinity'):
        version = io.parse_first_line(output_lines[0])

    ### rewrite infile
    print(program_name + '	' + version)

if __name__ == '__main__':
    main()
