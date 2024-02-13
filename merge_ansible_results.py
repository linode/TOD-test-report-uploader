from datetime import datetime
import os
import xml.etree.ElementTree as ET

def merge_xml_files(input_dir, output_file):
    # Create the root element for the new XML
    merged_testsuites = ET.Element('testsuites')

    merged_testsuite = ET.SubElement(merged_testsuites, 'testsuite')

    total_failures = 0
    total_skipped = 0
    total_errors = 0
    total_tests = 0

    # Iterate through each XML file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.xml'):
            filepath = os.path.join(input_dir, filename)
            tree = ET.parse(filepath)
            testsuite = tree.getroot().find('testsuite')

            total_failures += int(testsuite.get("failures"))
            total_skipped += int(testsuite.get("skipped"))
            total_errors += int(testsuite.get("errors"))
            total_tests += int(testsuite.get("tests"))

            # Iterate through each testcase in the testsuite and add failure message to the merged XML
            for testcase in testsuite.findall('testcase'):
                new_testcase = ET.SubElement(merged_testsuite, 'testcase')
                new_testcase.set('name', testsuite.get('name') + ": " + testcase.get('name'))
                failure = testcase.find('failure')
                if failure is not None:
                    failure_message = failure.get('message')
                    merged_testcase = ET.SubElement(merged_testsuite, 'testcase')
                    merged_testcase.set('name', testsuite.get('name') + ": " + testcase.get('name'))
                    failure_element = ET.SubElement(merged_testcase, 'failure')
                    failure_element.set('message', failure_message)

    merged_testsuite.set("failures", str(total_failures))
    merged_testsuite.set("skipped", str(total_skipped))
    merged_testsuite.set("errors", str(total_errors))
    merged_testsuite.set("tests", str(total_tests))
    merged_testsuite.set("name", "Ansible Merged XML")

    # Write the merged XML to the output file
    merged_tree = ET.ElementTree(merged_testsuites)
    merged_tree.write(output_file)


# Example usage specific to ansible repository
input_directory = os.path.join(os.getcwd(), "output/junit")
current_time = datetime.now()
output_xml_file = current_time.strftime("%Y%m%d%H%M") + '_ansible_merged.xml'
merge_xml_files(input_directory, output_xml_file)
