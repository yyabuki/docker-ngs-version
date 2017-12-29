import re

class IOUtil():

    def __init__(self, container_list):
        self.container_list = container_list
        self.container_info = {}

    def __init__(self):
        return None

    def read_container_list(self):
        with open(self.container_list, mode='r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                container_program = line.split('	')
                self.container_info[container_program[0]] = container_program[1]
        f.close()
        return self.container_info

    def get_results(self, output_file):
        output_lines = []
        with open(output_file, mode='r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if 'error' in line.lower():
                    continue
                output_lines.append(line)
        f.close()
        return output_lines

    ### for outputs in which 'Version:' tag exists.
    def parse_multiple_lines(self, output_lines, program_name):
        version = ''
        for line in output_lines:
            if line.startswith('Version:'):
                if program_name == 'annovar':
                    date_pattern = re.compile('(\d{4})\-(\d{2})\-(\d{2})')
                    result = date_pattern.search(line)
                    yyyy, mm, dd = result.groups()
                    version = yyyy + mm + dd
                elif program_name == 'samtools':
                    version = line.split()[1]
                else:
                    version = line.split(' ')[-1]
                break
            elif 'Sailfish' in line:
                version = re.sub('^v', '', line.split(' ')[-1])
                break
        return version

    ### for outputs in which the version number is written in first line.
    def parse_first_line(self, output_line):
        raw_version_str = output_line.split(' ')[-1]
        # for picard
        trim_version_str = re.sub('[\(\)]', '', raw_version_str)
        # for STAR
        trim_version_str = re.sub('^(STAR_)', '', trim_version_str)
        # for Trinity
        trim_version_str = re.sub('^(Trinity-)', '', trim_version_str)
        # delete first 'v'(version) if exists in
        trim_version_str = re.sub('^v', '', trim_version_str)
        version = trim_version_str
        return version

    ### make software - version number list.
    def make_version_list(self, versions, containers, version_list):
        with open(version_list, mode='w') as f:
            for program_name, version in sorted(versions.items()):
                f.write(containers[program_name] + '	' + program_name + '	' + version + '\n')
        f.close()

    ### rewrite infile
    def rewrite_infile(self, program_name, version, infile):
        with open(infile, mode='w') as f:
            f.write(program_name + '	' + version + '\n')
            f.close()
