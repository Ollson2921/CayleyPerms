from cayley_permutations import Av, CayleyPermutation
import json
from clouds import TrackedTileScopePack
from comb_spec_searcher import CombinatorialSpecification
from clouds.strategies.add_cloud import AddCloudsStrategy
from clouds.strategies.fusion import (
    TrackedFusionStrategy,
    TrackedFusionPointRowStrategy,
)
from comb_spec_searcher.strategies import Rule

# basis_desc = "3s_4x1"  # change descriptor to change file
basis_desc = "3s"

all_packs = TrackedTileScopePack.all_packs()

# Load bases from file
with open(f"fusion_to_run_{basis_desc}.txt", "r") as f:
    bases = eval(f.readline())

for basis in bases:
    for pack in all_packs:
        try:
            with open(f"specs/{Av(basis)}_{pack.name}.json", "r") as f:
                spec = json.load(f)
            spec = CombinatorialSpecification.from_dict(spec)
            eqns = spec.get_maple_equations()
            try:
                spec.get_genf()
                print(eqns)
                with open(
                    f"fusion_eqns_cayley_3s_run_2/{Av(basis)}_{pack.name}.txt", "w"
                ) as f:
                    f.write(eqns)
            except NotImplementedError:
                # continue
                all_rules = list(spec.rules_dict.values())
                new_all_rules = []
                for rule in all_rules:
                    if rule.get_op_symbol() == "⚮":
                        cloud_to_add = (rule.strategy.index,)
                        if (
                            rule.strategy.fuse_rows
                            and cloud_to_add in rule.comb_class.value_clouds
                            or not rule.strategy.fuse_rows
                            and cloud_to_add in rule.comb_class.indices_clouds
                        ):
                            new_all_rules.append(rule)
                            continue
                        add_cloud_strat = (
                            AddCloudsStrategy(
                                val_clouds=[[rule.strategy.index]], idx_clouds=[]
                            )
                            if rule.strategy.fuse_rows
                            else AddCloudsStrategy(
                                val_clouds=[], idx_clouds=[[rule.strategy.index]]
                            )
                        )
                        add_cloud_children = add_cloud_strat(rule.comb_class).children
                        add_cloud_rule = Rule(
                            add_cloud_strat,
                            rule.comb_class,
                            children=add_cloud_children,
                        )
                        new_all_rules.append(add_cloud_rule)
                        if rule.formal_step[:5] == "Point":
                            new_all_rules.append(
                                Rule(
                                    TrackedFusionPointRowStrategy(
                                        rule.strategy.fuse_rows, rule.strategy.index
                                    ),
                                    add_cloud_children[0],
                                    children=TrackedFusionPointRowStrategy(
                                        rule.strategy.fuse_rows, rule.strategy.index
                                    )(add_cloud_rule.comb_class).children,
                                )
                            )
                        elif rule.formal_step[:4] == "Fuse":
                            new_all_rules.append(
                                Rule(
                                    TrackedFusionStrategy(
                                        rule.strategy.fuse_rows, rule.strategy.index
                                    ),
                                    add_cloud_children[0],
                                    children=TrackedFusionStrategy(
                                        rule.strategy.fuse_rows, rule.strategy.index
                                    )(add_cloud_rule.comb_class).children,
                                )
                            )
                        else:
                            print("OH NOO")
                    else:
                        new_all_rules.append(rule)

                new_spec = CombinatorialSpecification(
                    spec.root, new_all_rules
                ).expand_verified()
                eqns = new_spec.get_maple_equations()

                with open(
                    f"fusion_eqns_cayley_3s_run_2/{Av(basis)}_{pack.name}.txt", "w"
                ) as f:
                    f.write(eqns)
                continue
            # try:
            #     spec.get_genf()
            # except NotImplementedError:
            #     input()
            #     continue
        except FileNotFoundError:
            continue
